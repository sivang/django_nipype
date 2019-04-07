from django.forms.models import model_to_dict
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from nipype.interfaces.base import Interface


class VertexConfiguration(TimeStampedModel, TitleDescriptionModel):
    NON_CONFIGURATION_FIELDS = [
        "id",
        "name",
        "title",
        "description",
        "created",
        "modified",
    ]
    CONFIGURATION_KEYS = dict()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.to_kwargs())

    def to_kwargs(self) -> dict:
        _dict = model_to_dict(self)
        config = {
            self.CONFIGURATION_KEYS.get(key, key): value
            for key, value in _dict.items()
            if key not in self.NON_CONFIGURATION_FIELDS and value
        }
        return config

    def create_interface(self) -> Interface:
        raise NotImplementedError
