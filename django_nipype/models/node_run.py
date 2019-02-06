from django.db import models
from django_nipype.models import NodeResults
from nipype.interfaces.base import CommandLine
from nipype.pipeline import Node


class NodeRun(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def build_command(self) -> CommandLine:
        raise NotImplementedError

    def create_node(self) -> Node:
        raise NotImplementedError

    def create_results_instance(self) -> NodeResults:
        raise NotImplementedError

    def run(self) -> NodeResults:
        raise NotImplementedError
