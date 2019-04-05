import os

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django_nipype.models.interfaces.fsl.bet.choices import Output
from django_nipype.models.vertex import Vertex
from django_nipype.models.interfaces.fsl.bet import BetOutput
from django_nipype.utils import jasonable_dict
from nipype.interfaces.fsl import BET


def default_output():
    return [BetRun.BRAIN]


class BetRun(Vertex):
    inputs = models.ForeignKey(
        "django_nipype.BetInput", on_delete=models.CASCADE, related_name="runs"
    )
    configuration = models.ForeignKey(
        "django_nipype.BetConfiguration", on_delete=models.PROTECT, related_name="runs"
    )
    output = models.OneToOneField(
        "django_nipype.BetOutput",
        on_delete=models.CASCADE,
        related_name="output_of",
        null=True,
    )

    log = JSONField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "FSL Brain Extraction Runs"

    def set_interface_input(self, interface: BET) -> BET:
        interface.inputs.in_file = self.inputs.nifti
        return interface

    def create_results_instance(self) -> BetOutput:
        outputs = self.get_output_dict()
        return BetOutput.objects.create(**outputs)

    def run(self):
        if not self.results:
            if not self.id:
                self.save()
            interface = self.create_interface()
            results = interface.run()
            self.log = jasonable_dict(results.runtime.dictcopy())
            self.results = self.create_results_instance()
            self.save()
        return self.results

    def delete(self):
        self.results.delete()
        super(BetRun, self).delete()
