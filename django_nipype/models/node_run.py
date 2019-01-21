from django.db import models


class NodeRun(models.Model):
    node_configuration = models.ForeignKey(
        "django_nipype.NodeConfiguration",
        on_delete=models.PROTECT,
        related_name="output",
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

