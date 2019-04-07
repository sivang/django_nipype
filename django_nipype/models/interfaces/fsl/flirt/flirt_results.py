# from django.conf import settings
# from django.db import models
# from django_nipype.models.vertex import VertexOutput


# class FlirtResults(VertexOutput):
#     out_file = models.FilePathField(
#         settings.MEDIA_ROOT, match="*.nii*", recursive=True, null=True, blank=True
#     )
#     log = models.FilePathField(
#         settings.MEDIA_ROOT, match="*.log", recursive=True, null=True, blank=True
#     )
#     matrix = models.FilePathField(
#         settings.MEDIA_ROOT, match="*.mat", recursive=True, null=True, blank=True
#     )

#     ON_DELETE = ["out_file", "log", "matrix"]

#     @property
#     def registered(self):
#         return self.out_file
