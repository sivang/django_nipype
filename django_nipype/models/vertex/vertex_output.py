import os

# from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django_extensions.db.models import TimeStampedModel


class VertexOutput(TimeStampedModel):
    run = models.ForeignKey(
        "django_nipype.Vertex", on_delete=models.CASCADE, related_name="output_set"
    )
    SHORT_DESCRIPTION = str()
    SHORT_DESCRIPTIONS = dict()

    def __str__(self) -> str:
        try:
            run_id = self.run.id
            description = self.get_output_display_name()
            if not description:
                return f"Vertex #{run_id} Results"
            return f"Vertex #{run_id} {description} Results"
        except (AttributeError, NotImplementedError):
            return f"VertexOutput #{self.id}"

    def get_output_display_name(self) -> str:
        try:
            return self.SHORT_DESCRIPTIONS.get(self.output_type, self.SHORT_DESCRIPTION)
        except AttributeError:
            return self.SHORT_DESCRIPTION

    class Meta:
        abstract = True


class VertexFileOutputManager(models.Manager):
    def get_or_create(self, **kwargs):
        try:
            return super().get_or_create(**kwargs)
        except MultipleObjectsReturned:
            if all(kwarg in kwargs for kwarg in ("run", "output_type")):
                return self.filter(**kwargs), False
            raise MultipleObjectsReturned


class VertexFileOutput(VertexOutput):
    path = models.FilePathField(unique=True)
    SUFFIX = dict()
    DEFAULT_SUFFIX = str()
    EXTENSION = dict()
    DEFAULT_EXTENSION = str()
    DEFAULT_INTERFACE_CONFIGURATION_VALUE = True
    INTERFACE_CONFIGURATION_KEYS = dict()
    INTERFACE_CONFIGURATION_VALUES = dict()

    objects = VertexFileOutputManager()

    class Meta:
        abstract = True

    def get_multiple_output_suffixes(self) -> list:
        try:
            return self.SUFFIX[self.output_type]
        except KeyError:
            raise NotImplementedError

    # def save(self, *args, **kwargs) -> None:
    #     try:
    #         self.path = self.path or self.get_default_path(**kwargs)
    #     except ValueError:
    #         model = apps.get_model(
    #             app_label="django_nipype", model_name=self.__class__.__name__
    #         )
    #         for suffix in self.get_multiple_output_suffixes():
    #             kwargs["path"] = self.get_default_path(suffix=suffix)
    #             # kwargs.pop("force_insert")
    #             # kwargs.pop("using")
    #             model.objects.get_or_create(**kwargs, run=self.run)
    #         return
    #     super().save(*args, **kwargs)

    def get_directory_path(self) -> str:
        try:
            return self.run.get_path()
        except AttributeError:
            raise NotImplementedError

    def get_base_name(self) -> str:
        try:
            return str(self.run.id)
        except AttributeError:
            raise NotImplementedError

    def get_suffix(self) -> str:
        try:
            suffix = self.SUFFIX.get(self.output_type, self.DEFAULT_SUFFIX)
        except AttributeError:
            raise NotImplementedError
        if isinstance(suffix, list):
            raise ValueError("Suffix must be defined as a string!")
        return suffix

    def get_extension(self) -> str:
        try:
            return self.EXTENSION.get(self.output_type, self.DEFAULT_EXTENSION)
        except AttributeError:
            raise NotImplementedError

    def get_default_file_name(self, **kwargs) -> str:
        base_name = kwargs.get("base_name") or self.get_base_name()
        suffix = kwargs.get("suffix") or self.get_suffix()
        extension = kwargs.get("extension") or self.get_extension()
        return f"{base_name}{suffix}.{extension}"

    def get_default_path(self, **kwargs) -> str:
        base_dir = self.get_directory_path()
        file_name = self.get_default_file_name(**kwargs)
        return os.path.join(base_dir, file_name)

    def get_interface_configuration(self) -> dict:
        try:
            key = self.INTERFACE_CONFIGURATION_KEYS.get(self.output_type)
            value = self.INTERFACE_CONFIGURATION_VALUES.get(
                self.output_type, self.DEFAULT_INTERFACE_CONFIGURATION_VALUE
            )
            return {key: value}
        except AttributeError:
            return dict()

    @property
    def exists(self) -> bool:
        return os.path.isfile(self.path)

    @property
    def interface_configuration(self) -> dict:
        return self.get_interface_configuration()
