import json
import os

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.forms.models import model_to_dict
from django_nipype.models.fields import ChoiceArrayField
from django_nipype.models.interfaces.fsl.bet import BetRun, BetOutput
from django_nipype.models.interfaces.fsl.bet.choices import Mode
from django_nipype.models.vertex import VertexConfiguration
from nipype.interfaces.fsl import BET


def default_output() -> list:
    return BetOutput.DEFAULT


class BetConfiguration(VertexConfiguration):
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
    mode = models.CharField(max_length=4, choices=Mode.choices(), default=Mode.NORMAL)
    base_output_name = models.CharField(max_length=55, blank=True, null=True)
    output = ChoiceArrayField(
        models.CharField(max_length=7, choices=BetOutput.choices()),
        size=5,
        blank=True,
        default=default_output,
    )

    class Meta:
        verbose_name_plural = "FSL BET Configurations"

    def __str__(self) -> str:
        return json.dumps(self.to_kwargs(), indent=2)

    def to_kwargs_without_mode(self) -> dict:
        d = model_to_dict(self)
        skip = ["id", "name", "mode", "title", "description", "created", "modified"]
        config = {
            self.CONFIG_DICT.get(key, key): value
            for key, value in d.items()
            if key not in skip and value
        }
        return config

    def add_mode_to_kwargs(self, config: dict) -> dict:
        if self.mode is not Mode.NORMAL:
            trait_name = self.get_mode_display().lower().replace(" ", "_")
            config[trait_name] = True
        return config

    def to_kwargs(self) -> dict:
        config = self.to_kwargs_without_mode()
        config = self.add_mode_to_kwargs(config)
        return config

    def create_interface(self) -> BET:
        config = self.to_kwargs()
        return BET(**config)

    def set_interface_output(self, interface: BET, run: BetRun) -> BET:
        for chosen_output in self.output:
            if chosen_output != "brain":
                setattr(interface.inputs, chosen_output, True)
            else:
                interface.inputs.out_file = run.output.get_default_path("brain")
        else:
            interface.inputs.no_output = True
        return interface

