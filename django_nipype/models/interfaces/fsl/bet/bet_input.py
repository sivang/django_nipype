from django.db import models
from django_nipype.models.vertex import VertexInput


class BetInput(VertexInput):
    nifti = models.ForeignKey(
        "mri.NIfTI", on_delete=models.CASCADE, related_name="as_bet_input"
    )

