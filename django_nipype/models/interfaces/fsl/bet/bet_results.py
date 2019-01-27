from django.conf import settings
from django.db import models
from django_nipype.models import NodeResults


class BetResults(NodeResults):
    brain = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.nii*", recursive=True
    )
    skull = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.nii*", recursive=True
    )
    binary_mask = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.nii*", recursive=True
    )
    outline = models.FilePathField(
        path=settings.MEDIA_ROOT, match="*.nii*", recursive=True
    )
    mesh = models.FilePathField(path=settings.MEDIA_ROOT, recursive=True)

    run = models.ForeignKey(
        "django_nipype.BetRun", on_delete=models.PROTECT, related_name="results"
    )

    class Meta:
        verbose_name_plural = "Results"

