from django.conf import settings
from django.db import models
from django_nipype.models import NodeResults


class FlirtResults(NodeResults):
    out_file = models.FilePathField(
        settings.MEDIA_ROOT, match="*.nii*", recursive=True, null=True, blank=True
    )
    # out_log = models.FilePathField(
    #     settings.MEDIA_ROOT, match="*.log", recursive=True, null=True, blank=True
    # )
    # out_martix_file = models.FilePathField(
    #     settings.MEDIA_ROOT, match="*.mat", recursive=True, null=True, blank=True
    # )

    @property
    def registered(self):
        return self.out_file
