from django.db import models

# from django_nipype.models import NodeRun


class Pipe(models.Model):
    source = models.ForeignKey("django_nipype.PipeSource", on_delete=models.CASCADE)
    destination = models.ForeignKey(
        "django_nipype.PipeDestination", on_delete=models.CASCADE
    )
    workflow = models.ManyToManyField("django_nipype.Workflow")
