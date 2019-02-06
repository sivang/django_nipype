import os

from django.db import models
from django.conf import settings
from django_nipype.models import NodeRun
from django_nipype.models.fields import ChoiceArrayField
from django_nipype.models.interfaces.fsl.bet import BetResults
from nipype.interfaces.fsl import BET
from nipype.pipeline import Node

BET_RESULTS = os.path.join(settings.MEDIA_ROOT, "nipype", "BET")


def default_output():
    return [BetRun.BRAIN]


class BetRun(NodeRun):
    in_file = models.FilePathField(
        path=settings.MEDIA_ROOT, max_length=255, match="*.nii*", recursive=True
    )
    configuration = models.ForeignKey(
        "django_nipype.BetConfiguration", on_delete=models.PROTECT, related_name="runs"
    )

    # Output files configuration
    BRAIN = "BRN"
    SURFACE_OUTLINE = "SRF"
    MASK = "MSK"
    SKULL = "SKL"
    MESH_SURFACE = "MSH"
    OUTPUT_CHOICES = (
        (BRAIN, "Brain"),
        (SURFACE_OUTLINE, "Surface Outline"),
        (MASK, "Binary Mask"),
        (SKULL, "Skull"),
        (MESH_SURFACE, "Mesh Surface"),
    )
    # Each possible output file has a corresponding trait in BET configuration
    OUTPUT_TRAIT_NAMES = {
        BRAIN: "out_file",
        SURFACE_OUTLINE: "outline",
        MASK: "mask",
        SKULL: "skull",
        MESH_SURFACE: "mesh",
    }
    OUTPUT_SUFFIX = {
        BRAIN: "",
        SURFACE_OUTLINE: "_overlay",
        MASK: "_mask",
        SKULL: "_skull",
        MESH_SURFACE: "_mesh",
    }
    output = ChoiceArrayField(
        models.CharField(max_length=3, choices=OUTPUT_CHOICES),
        size=5,
        blank=True,
        default=default_output,
    )

    results = models.OneToOneField(
        "django_nipype.BetResults",
        on_delete=models.PROTECT,
        related_name="results_for",
        null=True,
    )

    class Meta:
        verbose_name_plural = "Runs"

    def default_out_path(self, output_file=BRAIN) -> str:
        if output_file == self.MESH_SURFACE:
            extension = "vtk"
        else:
            extension = "nii.gz"
        return os.path.join(
            BET_RESULTS, f"{self.id}{self.OUTPUT_SUFFIX[output_file]}.{extension}"
        )

    def add_output_to_kwargs(self, config: dict) -> dict:
        for output_file in self.output:
            if output_file != self.BRAIN:
                trait_name = self.OUTPUT_TRAIT_NAMES[output_file]
                config[trait_name] = True
        return config

    def build_command(self) -> BET:
        config = self.configuration.create_kwargs()
        config = self.add_output_to_kwargs(config)
        return BET(**config)

    def create_node(self) -> Node:
        bet = self.build_command()
        node = Node(bet, name=f"bet_{self.id}_node")
        node.inputs.in_file = self.in_file
        node.inputs.out_file = self.default_out_path(self.BRAIN)
        # if self.output == []:
        #     node.inputs.no_output = True
        return node

    def create_results_instance(self) -> BetResults:
        self.results = BetResults()
        for output_file in self.output:
            setattr(
                self.results,
                self.OUTPUT_TRAIT_NAMES[output_file],
                self.default_out_path(output_file),
            )
        self.results.save()
        return self.results

    def run(self):
        if not self.id:
            self.save()
        node = self.create_node()
        node.run()
        self.create_results_instance()
        self.save()
        return self.results

    def delete(self):
        self.results.delete()
        super(BetRun, self).delete()
