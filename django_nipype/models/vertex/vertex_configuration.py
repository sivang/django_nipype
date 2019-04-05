from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from nipype.interfaces.base import Interface


class VertexConfiguration(TimeStampedModel, TitleDescriptionModel):
    class Meta:
        abstract = True

    def to_kwargs(self) -> dict:
        raise NotImplementedError

    def create_interface(self) -> Interface:
        raise NotImplementedError
