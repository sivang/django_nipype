from django.db import models
from django_nipype.apps import DjangoNipypeConfig
from django_nipype.models import NodeResults


class BetResults(NodeResults):
    brain = models.FilePathField(
        path=DjangoNipypeConfig.RESULTS_PATH, match="*.nii*", recursive=True
    )
    skull = models.FilePathField(
        path=DjangoNipypeConfig.RESULTS_PATH, match="*.nii*", recursive=True
    )
    binary_mask = models.FilePathField(
        path=DjangoNipypeConfig.RESULTS_PATH, match="*.nii*", recursive=True
    )
    outline = models.FilePathField(
        path=DjangoNipypeConfig.RESULTS_PATH, match="*.nii*", recursive=True
    )
    mesh = models.FilePathField(path=DjangoNipypeConfig.RESULTS_PATH, recursive=True)

    run = models.ForeignKey(
        "django_nipype.BetRun", on_delete=models.PROTECT, related_name="results"
    )
