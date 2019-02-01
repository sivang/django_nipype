import json

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.forms.models import model_to_dict
from django_nipype.models import NodeConfiguration


class BetConfiguration(NodeConfiguration):
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

    class Meta:
        verbose_name_plural = "BET Configurations"

    def __str__(self):
        return json.dumps(self.create_kwargs(), indent=2)

    def as_kwargs_without_mode(self) -> dict:
        d = model_to_dict(self)
        skip = ["id", "name", "mode"]
        config = {
            self.CONFIG_DICT.get(key, key): value
            for key, value in d.items()
            if key not in skip and value
        }
        return config

    def add_mode_to_kwargs(self, config: dict) -> dict:
        if self.mode:
            trait_name = self.get_mode_display().lower().replace(" ", "_")
            config[trait_name] = True
        return config

    def create_kwargs(self) -> dict:
        config = self.as_kwargs_without_mode()
        config = self.add_mode_to_kwargs(config)
        return config
