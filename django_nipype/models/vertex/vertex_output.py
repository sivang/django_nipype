import os

from django.db.models import models
from django_extensions.db.models import TimeStampedModel


class VertexOutput(TimeStampedModel):
    DEFAULT = list()
    CHOICES = list()
    NON_OUTPUT_FIELDS = ("id", "created", "modified")

    class Meta:
        abstract = True

    @classmethod
    def get_output_field_names(cls) -> list:
        return [
            field.name
            for field in cls._meta.fields
            if field.name not in cls.NON_OUTPUT_FIELDS
        ]

    @classmethod
    def get_output_paths(cls) -> list:
        return [
            field.path
            for field in cls._meta.fields
            if isinstance(field, models.FilePathField)
        ]

    @classmethod
    def choices(cls) -> tuple:
        return tuple(cls.CHOICES)

    def configure_interface(self):
        raise NotImplementedError

    def delete(self):
        for output_file in self.ON_DELETE:
            path = getattr(self, output_file)
            if path:
                try:
                    os.remove(path)
                except FileNotFoundError:
                    continue
        super(VertexOutput, self).delete()

