import os

from django.conf import settings
from django.apps import AppConfig


class DjangoNipypeConfig(AppConfig):
    name = "django_nipype"
    directory_name = "nipype"
    results_path = os.path.join(settings.MEDIA_ROOT, directory_name)
