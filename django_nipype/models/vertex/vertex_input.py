from django.db import models


class VertexInput(models.Model):
    NON_INPUT_FIELDS = ("id",)

    class Meta:
        abstract = True

    @classmethod
    def get_input_field_names(cls) -> list:
        return [
            field.name
            for field in cls._meta.fields
            if field.name not in cls.NON_INPUT_FIELDS
        ]
