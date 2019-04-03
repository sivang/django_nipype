import os

from django_extensions.db.models import TimeStampedModel


class NodeResults(TimeStampedModel):
    class Meta:
        abstract = True

    def delete(self):
        for output_file in self.ON_DELETE:
            path = getattr(self, output_file)
            if path:
                try:
                    os.remove(path)
                except FileNotFoundError:
                    continue
        super(NodeResults, self).delete()
