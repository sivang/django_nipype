from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.forms.models import model_to_dict
from django_nipype.models.fields import ChoiceArrayField
from django_nipype.models import NodeConfiguration
from nipype.interfaces.fsl import BET
from nipype.pipeline import Node


def default_output():
    return [BetConfiguration.BRAIN]


class BetConfiguration(NodeConfiguration):

    name = models.CharField(max_length=100, blank=True, null=True)

    # Skull stripping configuration
    CONFIG_DICT = {
        "fractional_intensity_threshold": "frac",
        "head_radius": "radius",
        "threshold_segmented": "threshold",
    }
    fractional_intensity_threshold = models.FloatField(
        default=0.5, help_text="Fractional intensity threshold"
    )
    vertical_gradient = models.FloatField(
        default=0,
        help_text="Vertical gradient in fractional intensity threshold (-1, 1)",
    )
    head_radius = models.PositiveIntegerField(
        help_text="Head radius in millimeters (mm)", blank=True, null=True
    )
    gravity_center = models.CharField(
        max_length=30,
        help_text="Initial mesh surface center of gravity in voxels",
        validators=[validate_comma_separated_integer_list],
        blank=True,
        null=True,
    )
    threshold_segmented = models.BooleanField(
        default=False, help_text="Apply thresholding to segmented brain image and mask"
    )

    # Mode configuration choices
    NORMAL = None
    ROBUST = "ROBU"
    PADDING = "PADD"
    REMOVE_EYES = "REMO"
    SURFACES = "SURF"
    FUNCTIONAL = "FUNC"
    REDUCE_BIAS = "REDU"
    MODE_CHOICES = (
        (NORMAL, "Normal"),
        (ROBUST, "Robust"),
        (PADDING, "Padding"),
        (REMOVE_EYES, "Remove Eyes"),
        (SURFACES, "Surfaces"),
        (FUNCTIONAL, "Functional"),
        (REDUCE_BIAS, "Reduce Bias"),
    )
    mode = models.CharField(
        max_length=4, choices=MODE_CHOICES, default=NORMAL, blank=True
    )

    # Output files configuration
    BRAIN = "BRN"
    SURFACE_OUTLINE = "SRF"
    BINARY_MASK = "MSK"
    SKULL = "SKL"
    MESH_SURFACE = "MSH"
    OUTPUT_CHOICES = (
        (BRAIN, "Brain"),
        (SURFACE_OUTLINE, "Surface Outline"),
        (BINARY_MASK, "Binary Mask"),
        (SURFACES, "Surfaces"),
        (FUNCTIONAL, "Functional"),
    )
    # Each possible output file has a corresponding trait in BET configuration
    OUTPUT_TRAITS = {
        BRAIN: "out_file",
        SURFACE_OUTLINE: "outline",
        BINARY_MASK: "mask",
        SKULL: "skull",
        MESH_SURFACE: "mesh",
    }
    output = ChoiceArrayField(
        models.CharField(max_length=3, choices=OUTPUT_CHOICES),
        size=5,
        blank=True,
        default=default_output,
    )

    class Meta:
        verbose_name_plural = "Configurations"

    def get_configuration_dict(self) -> dict:
        d = model_to_dict(self)
        skip = ["id", "name", "mode", "output"]
        config = {
            self.CONFIG_DICT.get(key, key): value
            for key, value in d.items()
            if key not in skip and value
        }
        return config

    def add_mode_to_config(self, config: dict) -> dict:
        if self.mode:
            trait_name = self.get_mode_display().lower().replace(" ", "_")
            config[trait_name] = True
        return config

    def add_output_to_config(self, config: dict) -> dict:
        for output_file in self.output:
            if output_file != self.BRAIN:
                trait_name = self.OUTPUT_TRAITS[output_file]
                config[trait_name] = True
        return config

    def create_kwargs(self) -> dict:
        config = self.get_configuration_dict()
        config = self.add_mode_to_config(config)
        config = self.add_output_to_config(config)
        return config

    def create_bet_instance(self) -> BET:
        return BET(**self.create_kwargs())

    def create_node(self) -> Node:
        bet = self.create_bet_instance()
        return Node(bet, name=self.name or "bet_node")
