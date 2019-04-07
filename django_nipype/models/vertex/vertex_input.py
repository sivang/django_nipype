import os

from django.db import models


class VertexInput(models.Model):
    run = models.ForeignKey(
        "django_nipype.Vertex", on_delete=models.CASCADE, related_name="output_set"
    )

    class Meta:
        abstract = True


class VertexFileInput(VertexInput):
    name = models.CharField(max_length=55, blank=True, null=True)
    path = models.FilePathField(max_length=500)

    class Meta:
        abstract = True

    def get_interface_configuration(self) -> dict:
        if self.name:
            return {self.name: self.path}
        return self.path

    @property
    def exists(self) -> bool:
        return os.path.isfile(self.path)

    @property
    def interface_configuration(self) -> dict:
        return self.get_interface_configuration()
