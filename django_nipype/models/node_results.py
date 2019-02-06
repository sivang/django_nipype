import os
from django.db import models


class NodeResults(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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
