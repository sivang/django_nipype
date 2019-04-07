import os

from django.db import models
from django.contrib.postgres.fields import JSONField
from django_nipype.models.vertex import Vertex
from django_nipype.models.interfaces.fsl.bet.bet_input import BetInput
from django_nipype.models.interfaces.fsl.bet.bet_output import BetOutput
from django_nipype.models.interfaces.fsl.bet.choices import Output
from django_nipype.utils import jasonable_dict
from nipype.interfaces.fsl import BET


class BetRun(Vertex):
    configuration = models.ForeignKey(
        "django_nipype.BetConfiguration",
        on_delete=models.PROTECT,
        related_name="run_set",
    )
    log = JSONField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "FSL BET Runs"

    def add_input(self, name: str, path: str):
        return BetInput.objects.get_or_create(name=name, path=path, run=self)[0]

    def set_interface_input(self, interface: BET) -> BET:
        for instance in self.input_set.all():
            try:
                for key, value in instance.interface_configuration.items():
                    setattr(interface.inputs, key, value)
            except (ValueError, AttributeError):
                raise RuntimeError(
                    f"Failed to set interface configuration for BET #{self.id}"
                )
        return interface

    def get_or_create_output_instances(self) -> list:
        instances = []
        for choice in self.configuration.output:
            instance, _ = BetOutput.objects.get_or_create(output_type=choice, run=self)
            instance = [instance] if isinstance(instance, BetOutput) else list(instance)
            instances += instance
        return instances

    def get_nonexistent_output_instances(self) -> list:
        return [
            output
            for output in self.get_or_create_output_instances()
            if not output.exists
        ]

    def set_interface_output(self, interface: BET) -> BET:
        non_existent = self.get_nonexistent_output_instances()
        brain, _ = BetOutput.objects.get_or_create(
            run=self, output_type=Output.BRN.name
        )
        if brain not in non_existent:
            non_existent += [brain]
        for instance in non_existent:
            for key, value in instance.interface_configuration.items():
                setattr(interface.inputs, key, value)
        return interface

    def run(self):
        if not self.id:
            self.save()
        if self.has_nonexistent_output:
            if not os.path.isdir(self.get_path()):
                self.create_path()
            interface = self.create_interface()
            results = interface.run()
            self.log = jasonable_dict(results.runtime.dictcopy())
            self.save()
        return self.output_set.all()

    @property
    def has_nonexistent_output(self) -> bool:
        return bool(self.get_nonexistent_output_instances())
