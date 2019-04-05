import os

from django.db import models
from django.conf import settings
from django_nipype.models.vertex import Vertex
from django_nipype.models.interfaces.fsl.flirt.flirt_results import FlirtResults
from nipype.interfaces.fsl import FLIRT
from nipype.pipeline import Node

FLIRT_RESULTS = os.path.join(settings.MEDIA_ROOT, "nipype", "FLIRT")


class FlirtRun(Vertex):
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
    output = models.OneToOneField(
        "django_nipype.FlirtResults",
        on_delete=models.PROTECT,
        related_name="output_of",
        null=True,
    )

    class Meta:
        verbose_name_plural = "FLIRT Runs"

    def default_out_path(self, extension: str = "nii.gz") -> str:
        return os.path.join(FLIRT_RESULTS, f"{self.id}.{extension}")

    def build_command(self):
        return FLIRT(**self.configuration.create_kwargs())

    def create_node(self) -> Node:
        flirt = self.build_command()
        return Node(flirt, name=f"flirt_{self.id}_node")

    def create_results_instance(self):
        kwargs = {"out_file": self.default_out_path()}
        if self.configuration.log:
            kwargs["log"] = self.default_out_path("log")
        if self.configuration.matrix:
            kwargs["matrix"] = self.default_out_path("mat")
        return FlirtResults.objects.create(**kwargs)

    def run(self):
        if not self.results:
            if not self.id:
                self.save()
            node = self.create_node()
            node.inputs.in_file = self.in_file
            node.inputs.reference = self.reference
            node.inputs.out_file = self.default_out_path()
            if self.configuration.log:
                node.inputs.out_log = self.default_out_path("log")
            if self.configuration.matrix:
                node.inputs.out_matrix_file = self.default_out_path("mat")
            node.run()
            self.results = self.create_results_instance()
            self.save()
        return self.results

    def delete(self):
        self.results.delete()
        super(FlirtRun, self).delete()
