import os

from django.db import models
from django.conf import settings
from django_nipype.models import NodeRun


BET_RESULTS = os.path.join(settings.MEDIA_ROOT, "nipype", "BET")


class BetRun(NodeRun):
    in_file = models.FilePathField(
        path=settings.MEDIA_ROOT, max_length=255, match="*.nii*", recursive=True
    )
    configuration = models.ForeignKey(
        "django_nipype.BetConfiguration", on_delete=models.PROTECT, related_name="runs"
    )

    class Meta:
        verbose_name_plural = "Runs"

    def default_out_path(self) -> str:
        if not self.id:
            self.save()
        return os.path.join(BET_RESULTS, f"{self.id}.nii.gz")

    def run(self):
        node = self.configuration.create_node()
        node.inputs.in_file = self.in_file
        if self.configuration.BRAIN in self.configuration.output:
            node.inputs.out_file = self.default_out_path()
        elif self.configuration.output == []:
            node.inputs.no_output = True
        return node.run()
