from django.db import models
from django_nipype.models.vertex import VertexFileInput


class BetInput(VertexFileInput):
    run = models.ForeignKey(
        "django_nipype.BetRun", on_delete=models.PROTECT, related_name="input_set"
    )
