from django.contrib.postgres.fields import ArrayField
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.forms.models import model_to_dict
from django_nipype.models import NodeConfiguration


class BetConfiguration(NodeConfiguration):

    CONFIG_DICT = {
        "output_surface_outline": "outline",
        "output_binary_mask": "mask",
        "output_skull": "skull",
        "output_mesh_surface": "mesh",
        "fractional_intensity_threshold": "frac",
        "head_radius": "radius",
        "threshold_segmented": "threshold",
    }

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

    # Skull stripping configuration
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
    mode = models.CharField(max_length=4, choices=MODE_CHOICES, default=NORMAL)

    # Output files configuration

    output_files = ArrayField(models.CharField(max_length=20), size=5)
    output_surface_outline = models.BooleanField(
        default=False, help_text="Create surface outline image"
    )
    output_binary_mask = models.BooleanField(
        default=False, help_text="Create binary mask image"
    )
    output_skull = models.BooleanField(default=False, help_text="Create skull image")
    output_mesh_surface = models.BooleanField(
        default=False, help_text="Generate a VTK mesh brain surface"
    )
    no_output = models.BooleanField(
        default=False, help_text="Don't generate segmented output"
    )

    class Meta:
        verbose_name_plural = "Configurations"

    def create_kwargs(self):
        d = model_to_dict(self)
        skip = ["id", "name", "mode"]
        kwargs = {
            self.CONFIG_DICT.get(key, key): value
            for key, value in d.items()
            if key not in skip and value
        }
        if self.mode:
            trait_name = self.get_mode_display().lower()
            kwargs[trait_name] = True
        return kwargs
