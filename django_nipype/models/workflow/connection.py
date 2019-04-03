from django.db import models

# from django_nipype.models import NodeRun


class Connection(models.Model):
    source = models.ForeignKey(
        "django_nipype.ConnectionSource", on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        "django_nipype.ConnectionDestination", on_delete=models.CASCADE
    )
    workflow = models.ManyToManyField("django_nipype.Workflow")

    # def get_connection_call(self) -> tuple:
    #     source_node = self.source.create_node()
    #     destination_node = self.destination.create_node()
    #     connections = list(zip(source_node.field_names, destination_node.field_names))
    #     return (source_node, destination_node, connections)

