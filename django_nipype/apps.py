from django.apps import AppConfig


class DjangoNipypeConfig(AppConfig):
    name = "django_nipype"
    DB_PATH = "/export/home/zvibaratz/Projects/pylabber/media/MRI"
    RESULTS_PATH = "/export/home/zvibaratz/Projects/pylabber/media/nipype"
