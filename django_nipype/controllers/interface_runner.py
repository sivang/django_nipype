import os

from django_analysis.models import Analysis, Run
from django_nipype.apps import DjangoNipypeConfig
from django_nipype.controllers.nipype_interface import NipypeInterface
from nipype.interfaces.base import InterfaceResult


class InterfaceRunner:
    def __init__(self, interface: NipypeInterface):
        self.interface = interface
        self.analysis, self.created_new_analysis = self.get_or_create_analysis()
        self.run_instance, self.created_new_run = self.get_or_create_run()

    def get_or_create_analysis(self) -> Analysis:
        return Analysis.objects.get_or_create(title=self.interface.analysis_name)

    def get_or_create_run(self) -> Run:
        return Run.objects.get_or_create(
            analysis=self.analysis,
            input_configuration=self.input_configuration,
            analysis_configuration=self.full_analysis_configuration,
        )

    def get_missing_output_configuration(self) -> list:
        if self.created_new_run or not self.run_instance.output:
            return self.output_configuration
        return {
            key: value
            for key, value in self.output_configuration.items()
            if self.interface.get_output_key(key) not in self.existing_output_keys
        }

    def update_run_output_configuration(self, output: dict):
        created = {}
        for output_configuration, output_key in self.interface.OUTPUT_KEYS.items():
            if isinstance(output_key, str) and output_key in output:
                created.update({output_configuration: True})
            elif isinstance(output_key, list) and [key in output for key in output_key]:
                created.update({output_configuration: True})
        try:
            self.run_instance.output_configuration.update(created)
        except AttributeError:
            self.run_instance.output_configuration = created

    def fix_interface_output(self, output: dict) -> dict:
        """
        Patch nipype's OutputSpec bug where the output paths are in the PWD
        instead of their actual location (with the out_file).
        """
        base_path = output.get(self.interface.BASE_OUTPUT_KEY)
        base_dir = os.path.dirname(base_path)
        for key in output:
            file_name = os.path.basename(output[key])
            # Fix out_file path created without .nii.gz suffix
            if key == self.interface.BASE_OUTPUT_KEY and len(file_name.split(".")) is 1:
                output[key] = output[key] + ".nii.gz"
            else:
                output[key] = os.path.join(base_dir, file_name)
        return output

    def update_run_output(self, output: dict) -> None:
        try:
            self.run_instance.output.update(output)
        except AttributeError:
            self.run_instance.output = output

    def update_run_instance(self, results: InterfaceResult) -> None:
        output = results.outputs.get_traitsfree()
        output = self.fix_interface_output(output)
        self.update_run_output_configuration(output)
        self.update_run_output(output)
        self.run_instance.save()

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

    def run(self) -> dict:
        destination = self.get_default_output_destination()
        missing_output = self.get_missing_output_configuration()
        results = self.interface.run(destination, output_configuration=missing_output)
        self.update_run_instance(results)

    @property
    def input_configuration(self) -> dict:
        return self.interface.configuration.input_configuration

    @property
    def analysis_configuration(self) -> dict:
        return self.interface.configuration.analysis_configuration

    @property
    def full_analysis_configuration(self) -> dict:
        return self.interface.configuration.get_full_analysis_configuration()

    @property
    def output_configuration(self) -> dict:
        return self.interface.configuration.output_configuration

    @property
    def expected_output_keys(self) -> list:
        return self.interface.get_expected_output_keys()

    @property
    def existing_output_keys(self) -> list:
        return self.run_instance.get_existing_output_keys(validate_paths=True)

    @property
    def has_missing_output(self) -> bool:
        return bool(self.get_missing_output_keys())
