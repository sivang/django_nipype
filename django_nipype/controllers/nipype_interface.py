from nipype.interfaces.base import BaseInterface, InterfaceResult
from nipype.interfaces.fsl import BET
from .configuration_parser import ConfigurationParser


class NipypeInterface:
    INPUT_KEYS = ["in_file"]
    OUTPUT_KEYS = {}
    BASE_OUTPUT_CONFIGURATION_KEY = "out_file"
    BASE_OUTPUT_KEY = "out_file"
    OUTPUT_TYPE_KEY = "output_type"
    IGNORE_KEYS = ["trait_added", "trait_modified"]

    def __init__(self, base: BaseInterface, **kwargs):
        self.base = base
        self._base_instance = base()
        self.configuration = ConfigurationParser(self, kwargs)

    def get_default_analysis_configuration(self) -> dict:
        return {
            key: value.default
            for key, value in self.base_traits.items()
            if key in self.configuration.get_analysis_configuration_keys()
        }

    def get_output_key(self, output_configuration_key: str) -> str:
        return self.OUTPUT_KEYS.get(output_configuration_key, output_configuration_key)

    def get_expected_output_configuration_keys(self) -> list:
        return list(
            set(
                [
                    key
                    for key, value in self.configuration.output_configuration.items()
                    if value is True
                ]
                + [self.BASE_OUTPUT_CONFIGURATION_KEY]
            )
        )

    def get_expected_output_keys(self) -> list:
        return [
            self.get_output_key(key) or key
            for key in self.get_expected_output_configuration_keys()
        ]

    def configure_base_instance(self, output_configuration: dict = None) -> None:
        input_configuration = self.configuration.input_configuration
        analysis_configuration = self.configuration.analysis_configuration
        output_configuration = (
            output_configuration or self.configuration.output_configuration
        )
        configuration = {
            **input_configuration,
            **analysis_configuration,
            **output_configuration,
        }
        for key, value in configuration.items():
            setattr(self.base_instance.inputs, key, value)

    def run(self, destination: str, output_configuration: dict = {}) -> InterfaceResult:
        self.configure_base_instance(output_configuration=output_configuration)
        setattr(
            self.base_instance.inputs, self.BASE_OUTPUT_CONFIGURATION_KEY, destination
        )
        return self.base_instance.run()

    @property
    def analysis_name(self) -> str:
        return self.base.__name__

    @property
    def base_instance(self) -> BaseInterface:
        if not isinstance(self._base_instance, BaseInterface):
            self._base_instance = self.base()
        return self._base_instance

    @property
    def base_traits(self) -> dict:
        return self.base.input_spec.class_traits()


class BetWrapper(NipypeInterface):
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
        "skull": [],
        "no_output": [],
    }

    def __init__(self, **kwargs):
        super().__init__(BET, **kwargs)

