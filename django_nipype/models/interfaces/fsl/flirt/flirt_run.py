import os

from django.db import models
from django.conf import settings
from django_nipype.models import NodeRun
from nipype.interfaces.fsl import FLIRT
from nipype.pipeline import Node

FLIRT_RESULTS = os.path.join(settings.MEDIA_ROOT, "nipype", "FLIRT")


class FlirtRun(NodeRun):
    in_file = models.FilePathField(
        path=settings.MEDIA_ROOT, max_length=255, match="*.nii*", recursive=True
    )
    reference = models.FilePathField(
        path=settings.MEDIA_ROOT, max_length=255, match="*.nii*", recursive=True
    )
    configuration = models.ForeignKey(
        "django_nipype.FlirtConfiguration",
        on_delete=models.PROTECT,
        related_name="runs",
    )
    results = models.OneToOneField(
        "django_nipype.FlirtResults",
        on_delete=models.PROTECT,
        related_name="results_for",
        null=True,
    )

    class Meta:
        verbose_name_plural = "FLIRT Runs"

    def default_out_path(self, extension: str = "nii.gz") -> str:
        return os.path.join(FLIRT_RESULTS, f"{self.id}.{extension}")

    def build_pipe(self):
        return FLIRT(**self.configuration.create_kwargs())

    def create_node(self) -> Node:
        flirt = self.build_pipe()
        return Node(flirt, name=f"flirt_{self.id}_node")

    def run(self):
        if not self.id:
            self.save()
        node = self.create_node()
        node.inputs.in_file = self.in_file
        node.inputs.reference = self.reference
        node.inputs.out_file = self.default_out_path()
        if self.configuration.log:
            node.inputs.out_log = self.default_out_path("log")
        return node.run()
