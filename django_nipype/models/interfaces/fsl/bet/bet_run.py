import os

from django.db import models
from django_nipype.apps import DjangoNipypeConfig
from django_nipype.models import NodeRun
from nipype.interfaces.fsl import BET


BET_DIR = os.path.join(DjangoNipypeConfig.RESULTS_PATH, "BET")


class BetRun(NodeRun):
    in_file = models.FilePathField(
        path=DjangoNipypeConfig.DB_PATH, max_length=255, match="*.nii*", recursive=True
    )

    configuration = models.ForeignKey(
        "django_nipype.BetConfiguration",
        on_delete=models.PROTECT,
        related_name="existing_runs",
    )

    class Meta:
        verbose_name_plural = "Runs"

    def create_out_file_path(self):
        file_name = f"{self.id}.nii.gz"
        os.makedirs(BET_DIR, exist_ok=True)
        return os.path.join(BET_DIR, file_name)

    def run(self):
        config = self.configuration.create_kwargs()
        bet = BET(**config)
        bet.inputs.in_file = self.in_file
        bet.inputs.out_file = self.create_out_file_path()
        bet.run()
