import os

from django_analysis.models import Analysis, Run
from django_nipype.apps import DjangoNipypeConfig
from django_nipype.utils import jsonable_dict
from nipype.interfaces.base import BaseInterface, InterfaceResult
from nipype.interfaces.fsl import BET


class RunAnalysis:
    INTERFACE = None
    INPUT_KEYS = ["in_file"]
    OUTPUT_KEYS = {}
    BASE_OUTPUT_KEY = "out_file"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.analysis, self.is_new_analysis = self.get_or_create_analysis()
        self.input_configuration = self.get_configuration(of_type="input")
        self.run_configuration = self.get_configuration(of_type="run")
        self.output_configuration = self.get_configuration(of_type="output")
        self.run_instance, self.is_new_run = self.get_or_create_run()

    def get_or_create_analysis(self) -> Analysis:
        try:
            return Analysis.objects.get_or_create(title=self.INTERFACE.__name__)
        except AttributeError:
            raise NotImplementedError(
                "Failed to get analysis name from interface class!"
            )

    def get_keys(self, of_type: str = "") -> list:
        if of_type == "input":
            return self.INPUT_KEYS
        elif of_type == "output":
            return list(self.OUTPUT_KEYS.keys())
        elif not of_type or of_type == "run":
            return [
                key
                for key in self.kwargs
                if key not in self.INPUT_KEYS and key not in self.OUTPUT_KEYS
            ]

    def get_configuration(self, of_type: str = "") -> dict:
        keys = self.get_keys(of_type=of_type)
        return {key: self.kwargs.get(key) for key in keys if key in self.kwargs}

    def get_or_create_run(self) -> Run:
        return Run.objects.get_or_create(
            analysis=self.analysis,
            configuration=self.run_configuration,
            input_configuration=self.input_configuration,
        )

    def create_interface_instance(self) -> BaseInterface:
        try:
            return self.INTERFACE()
        except TypeError:
            raise NotImplementedError("Failed to instantiate analysis interface!")

    def has_missing_output(self) -> bool:
        if not self.run_instance.output:
            return True
        for output in self.output_configuration:
            output_key = self.OUTPUT_KEYS[output]
            if isinstance(output_key, str):
                existing_output = self.run_instance.output.get(output_key, "")
                if not os.path.isfile(existing_output):
                    return True
            elif isinstance(output_key, list):
                output_paths = [self.run_instance.output.get(key) for key in output_key]
                existing_output = [os.path.isfile(path) for path in output_paths]
                return not all(existing_output)
            else:
                raise ValueError(
                    f"Invalid output key configuration ({output_key})! Value must be of type str or list."
                )

    def get_missing_output(self) -> dict:
        try:
            return {
                output: config
                for output, config in self.output_configuration.items()
                if not os.path.isfile(
                    self.run_instance.output.get(self.OUTPUT_KEYS[output], "")
                )
                and config is True
            }
        except AttributeError:
            return self.output_configuration

    def configure_interface_input(self, interface: BaseInterface) -> None:
        for key, value in self.input_configuration.items():
            setattr(interface.inputs, key, value)

    def configure_interface(self, interface: BaseInterface) -> None:
        for key, value in self.run_configuration.items():
            setattr(interface.inputs, key, value)

    def configure_interface_output(self, interface: BaseInterface) -> None:
        destination = self.set_output_destination(interface)
        missing_output = self.get_missing_output()
        if missing_output and self.BASE_OUTPUT_KEY not in missing_output:
            missing_output[self.BASE_OUTPUT_KEY] = destination
        for key, value in missing_output.items():
            setattr(interface.inputs, key, value)

    def apply_configuration(self, interface: BaseInterface) -> None:
        self.configure_interface_input(interface)
        self.configure_interface(interface)
        self.configure_interface_output(interface)

    def create_configured_interface_instance(self) -> BaseInterface:
        interface = self.create_interface_instance()
        self.apply_configuration(interface)
        return interface

    def get_default_output_directory(self) -> str:
        base_dir = DjangoNipypeConfig.results_path
        return os.path.join(base_dir, self.analysis.title, str(self.run_instance.id))

    def create_default_output_directory(self) -> str:
        path = self.get_default_output_directory()
        exist_ok = False
        if self.run_instance.output or self.run_instance.log:
            exist_ok = True
        os.makedirs(path, exist_ok=exist_ok)
        return path

    def get_default_output_destination(self) -> str:
        base_dir = self.create_default_output_directory()
        return os.path.join(base_dir, str(self.run_instance.id))

    def set_output_destination(self, interface: BaseInterface) -> str:
        destination = self.get_default_output_destination()
        setattr(interface.inputs, self.BASE_OUTPUT_KEY, destination)
        return destination

    def run_interface(self):
        instance = self.create_configured_interface_instance()
        return instance.run()

    def update_run_output_config(self):
        new_output_config = self.get_missing_output()
        try:
            self.run_instance.output_configuration.update(new_output_config)
        except AttributeError:
            self.run_instance.output_configuration = new_output_config

    def fix_interface_output(self, output: dict) -> dict:
        base_path = output.get(self.BASE_OUTPUT_KEY)
        base_dir = os.path.dirname(base_path)
        for key in output:
            file_name = os.path.basename(output[key])
            if key == self.BASE_OUTPUT_KEY and len(file_name.split(".")) is 1:
                output[key] = output[key] + ".nii.gz"
            else:
                output[key] = os.path.join(base_dir, file_name)
        return output

    def update_run_output(self, results: InterfaceResult):
        new_output = results.outputs.get_traitsfree()
        new_output = self.fix_interface_output(new_output)
        try:
            self.run_instance.output.update(new_output)
        except AttributeError:
            self.run_instance.output = new_output

    def update_run_instance(self, results: InterfaceResult):
        self.update_run_output_config()
        self.update_run_output(results)
        self.run_instance.log = jsonable_dict(results.runtime.dictcopy())
        self.run_instance.save()

    def run(self):
        if self.has_missing_output():
            results = self.run_interface()
            self.update_run_instance(results)
        return self.run_instance


class RunBET(RunAnalysis):
    INTERFACE = BET
    OUTPUT_KEYS = {
        "mask": "mask_file",
        "mesh": "meshfile",
        "outline": "outline_file",
        "surfaces": [
            "meshfile",
            "inskull_mask_file",
            "inskull_mesh_file",
            "outskull_mask_file",
            "outskull_mesh_file",
            "outskin_mask_file",
            "outskin_mesh_file",
            "skull_mask_file",
        ],
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

