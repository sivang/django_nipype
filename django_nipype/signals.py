# from django.apps import apps
from django.db.models.signals import pre_save
from django.dispatch import receiver

# from django_nipype.models.vertex.vertex_output import VertexOutput


@receiver(pre_save, sender="django_nipype.VertexOutput")
def pre_save_vertex_output_model_receiver(sender, instance, *args, **kwargs):
    try:
        instance.path = instance.path or instance.get_default_path(**kwargs)
    except ValueError:
        # model = apps.get_model(
        #     app_label="django_nipype", model_name=instance.__class__.__name__
        # )
        for suffix in instance.get_multiple_output_suffixes():
            kwargs["path"] = instance.get_default_path(suffix=suffix)
            sender.objects.get_or_create(**kwargs)

