from django.db import models
from django_nipype.apps import DjangoNipypeConfig
from django_nipype.models import NodeRun


class BetRun(NodeRun):
    in_file = models.FilePathField(
        path=DjangoNipypeConfig.DB_PATH, max_length=255, match="*.nii*", recursive=True
    )

    configuration = models.ForeignKey(
        "django_nipype.BetConfiguration",
        on_delete=models.PROTECT,
        related_name="existing_runs",
    )
    results = models.ForeignKey(
        "django_nipype.BetResults", on_delete=models.PROTECT, related_name="results_for"
    )
