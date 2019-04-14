from django_analysis.models import Analysis, Run
from django_nipype.controllers.nipype_interface import NipypeInterface


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

    def get_missing_output_configuration_keys(self) -> list:
        if self.created_new_run or not self.run_instance.output:
            return [key for key, config in self.output_configuration.items() if config]
        return [
            value
            for value in self.expected_output_keys
            if value not in self.existing_output_keys
        ]

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
