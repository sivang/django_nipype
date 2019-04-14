class ConfigurationException(Exception):
    pass


class ConfigurationParser:
    CONFIGURATION_TYPES = ("input", "analysis", "output")

    def __init__(self, interface, configuration: dict):
        self.interface = interface
        self.raw = configuration

    def get_base_output_key(self) -> str:
        try:
            return self.interface.BASE_OUTPUT_KEY
        except AttributeError:
            raise ConfigurationException(
                f"Failed to get base output key name from {self.interface}! Please make sure the BASE_OUTPUT_KEY class attribute is set."
            )

    def get_input_configuration_keys(self) -> list:
        try:
            return self.interface.INPUT_KEYS
        except AttributeError:
            raise ConfigurationException(
                f"Failed to get input keys from {self.interface}! Please make sure the INPUT_KEYS class attribute is set."
            )

    def get_output_keys_configuration(self) -> dict:
        try:
            return self.interface.OUTPUT_KEYS
        except AttributeError:
            raise ConfigurationException(
                f"Failed to get output keys from {self.interface}! Please make sure the OUTPUT_KEYS class attribute is set."
            )

    def get_ignorable_keys(self) -> list:
        try:
            return self.interface.IGNORE_KEYS
        except AttributeError:
            return []

    def get_output_configuration_keys(self) -> list:
        output_dict = self.get_output_keys_configuration()
        return list(output_dict.keys()) + [self.get_base_output_key()]

    def get_analysis_configuration_keys(self) -> list:
        input_keys = self.get_input_configuration_keys()
        output_keys = self.get_output_configuration_keys()
        ignore = self.get_ignorable_keys() + input_keys + output_keys
        return [key for key in self.interface.base_traits.keys() if key not in ignore]

    def get_configuration_keys(self, of_type: str = "") -> list:
        if of_type == "input":
            return self.get_input_configuration_keys()
        elif of_type == "output":
            return self.get_output_configuration_keys()
        elif not of_type or of_type == "analysis":
            return self.get_analysis_configuration_keys()

    def filter_configuration_by_type(
        self, configuration: dict, _type: str = ""
    ) -> dict:
        keys = self.get_configuration_keys(of_type=_type)
        return {key: value for key, value in configuration.items() if key in keys}

    def get_full_analysis_configuration(self) -> dict:
        default_configuration = self.interface.get_default_analysis_configuration()
        return {
            key: self.analysis_configuration.get(key, default_configuration.get(key))
            for key in self.get_analysis_configuration_keys()
        }

    @property
    def input_configuration(self) -> dict:
        return self.filter_configuration_by_type(self.raw, "input")

    @property
    def analysis_configuration(self) -> dict:
        return self.filter_configuration_by_type(self.raw, "analysis")

    @property
    def full_analysis_configuration(self) -> dict:
        return self.get_full_analysis_configuration()

    @property
    def output_configuration(self) -> dict:
        return self.filter_configuration_by_type(self.raw, "output")
