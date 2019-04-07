import os

from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_nipype.apps import DjangoNipypeConfig


class Vertex(TimeStampedModel):
    configuration = models.ForeignKey(
        "django_nipype.VertexConfiguration",
        on_delete=models.PROTECT,
        related_name="run_set",
    )

    class Meta:
        abstract = True

    def get_path(self) -> str:
        return os.path.join(
            settings.MEDIA_ROOT, DjangoNipypeConfig.name, self.__class__.__name__
        )

    def create_path(self) -> None:
        path = self.get_path()
        os.makedirs(path)

    def add_input(self, **kwargs):
        raise NotImplementedError

    def set_interface_input(self, interface):
        raise NotImplementedError

    def set_interface_output(self, interface):
        pass

    def configure_interface(self, interface):
        interface = self.set_interface_input(interface)
        return self.set_interface_output(interface)

    def create_interface(self):
        interface = self.configuration.create_interface()
        return self.configure_interface(interface)

    def run(self):
        raise NotImplementedError

    def create_results_instance(self):
        raise NotImplementedError
