import os

from django.conf import settings
from django.db import models
from django_nipype.models.interfaces.fsl.bet import BetRun
from django_nipype.models.vertex import VertexOutput

# from nipype.interfaces.fsl import BET


class BetOutput(VertexOutput):
    brain = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.nii*", recursive=True, null=True, blank=True
    )
    skull = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.nii*", recursive=True, null=True, blank=True
    )
    mask = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.nii*", recursive=True, null=True, blank=True
    )
    outline = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.nii*", recursive=True, null=True, blank=True
    )
    mesh = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.vtk", recursive=True, null=True, blank=True
    )

    DEFAULT = ["brain"]
    ON_DELETE = ["brain", "skull", "mask", "outline", "mesh"]
    CHOICES = [
        ("brain", "Brain"),
        ("skull", "Skull"),
        ("mask", "Mask"),
        ("outline", "Surface Outline"),
        ("mesh", "Mesh Surface"),
    ]
    SUFFIX = {
        "brain": "",
        "outline": "_overlay",
        "mask": "_mask",
        "skull": "_skull",
        "mesh": "_mesh",
    }

    class Meta:
        verbose_name_plural = "FSL BET Output"

    def get_default_file_name(self, field: models.FilePathField) -> str:
        suffix = self.SUFFIX.get(field.name, "_" + field.name)
        extension = "vtk" if field.name == "mesh" else "nii.gz"
        return f"{self.output_of.id}{suffix}.{extension}"

    def get_default_path(self, field: models.FilePathField) -> str:
        vertex_path = self.output_of.get_path()
        file_name = self.get_default_file_name(field)
        return os.path.join(vertex_path, file_name)
