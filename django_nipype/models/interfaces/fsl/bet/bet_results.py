from django.conf import settings
from django.db import models
from django_nipype.models import NodeResults


class BetResults(NodeResults):
    out_file = models.FilePathField(
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

    ON_DELETE = ["out_file", "skull", "mask", "outline", "mesh"]

    class Meta:
        verbose_name_plural = "Results"

    @property
    def brain(self):
        return self.out_file

