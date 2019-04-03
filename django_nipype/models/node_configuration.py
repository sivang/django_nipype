from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from nipype.interfaces.base import CommandLine
from nipype.pipeline import Node


class NodeConfiguration(TimeStampedModel, TitleDescriptionModel):
    class Meta:
        abstract = True

    def create_kwargs(self) -> dict:
        raise NotImplementedError("Abstract class method")

    def build_pipe(self) -> CommandLine:
        raise NotImplementedError("Abstract class method")

    def create_node(self) -> Node:
        raise NotImplementedError("Abstract class method")
