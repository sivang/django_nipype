from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Vertex(TitleDescriptionModel, TimeStampedModel):
    class Meta:
        abstract = True
