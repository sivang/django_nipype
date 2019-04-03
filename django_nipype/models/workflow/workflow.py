from django.contrib.postgres.fields import JSONField
from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Workflow(TitleDescriptionModel, TimeStampedModel):
    inputs = JSONField()

    def get_source_nodes(self) -> models.QuerySet:
        destinations = self.connection_set.values_list("destination", flat=True)
        try:
            self.connection_set.exclude(source__in=destinations)
        except models.ObjectDoesNotExist:
            raise RuntimeError("Failed to resolve workflow source node!")
