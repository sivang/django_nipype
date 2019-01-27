from django.db import models
from nipype.interfaces.base import CommandLine
from nipype.pipeline import Node


class NodeConfiguration(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def create_kwargs(self) -> dict:
        raise NotImplementedError("Abstract class method")

    def build_pipe(self) -> CommandLine:
        raise NotImplementedError("Abstract class method")

    def create_node(self) -> Node:
        raise NotImplementedError("Abstract class method")
