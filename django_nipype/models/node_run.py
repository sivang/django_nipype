from django_extensions.db.models import TimeStampedModel
from django_nipype.models import NodeResults
from nipype.interfaces.base import CommandLine
from nipype.pipeline import Node


class NodeRun(TimeStampedModel):
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
