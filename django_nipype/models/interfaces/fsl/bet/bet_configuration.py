from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django_nipype.models import NodeConfiguration


class BetConfiguration(NodeConfiguration):

    CONFIG_DICT = {
        "outline": "output_surface_outline",
        "mask": "output_binary_mask",
        "skull": "output_skull",
        "mesh": "output_mesh_surface",
        "frac": "fractional_intensity_threshold",
        "radius": "head_radius",
        "threshold": "segmentation_threshold",
    }

    # Skull stripping configuration
    fractional_intensity_threshold = models.FloatField(
        default=0.5, help_text="Fractional intensity threshold"
    )
    vertical_gradient = models.FloatField(
        default=0,
        help_text="Vertical gradient in fractional intensity threshold (-1, 1)",
    )
    head_radius = models.PositiveIntegerField(
        help_text="Head radius in millimeters (mm)"
    )
    gravity_center = models.CharField(
        help_text="Initial mesh surface center of gravity in voxels",
        validators=[validate_comma_separated_integer_list],
        blank=True,
        null=True,
    )
    segmentation_threshold = models.BooleanField(
        default=False, help_text="Apply thresholding to segmented brain image and mask"
    )

    # Output files configuration
    output_surface_outline = models.BooleanField(
        default=False, help_text="Create surface outline image"
    )
    output_binary_mask = models.BooleanField(
        default=False, help_text="Create binary mask image"
    )
    output_skull = models.BooleanField(default=False, help_text="Create skull image")
    no_output = models.BooleanField(
        default=False, help_text="Don't generate segmented output"
    )
    output_mesh_surface = models.BooleanField(
        default=False, help_text="Generate a VTK mesh brain surface"
    )

    # Modes
    robust = models.BooleanField(
        default=False,
        help_text="Robust brain center estimation (iterates BET several times)",
    )
    padding = models.BooleanField(
        default=False,
        help_text="Improve BET estimation if Field of View (FOV) is very small in Z (by temporarily padding end slices)",
    )
    remove_eyes = models.BooleanField(
        default=False, help_text="Remove eye and optic nerve"
    )
    surfaces = models.BooleanField(
        default=False,
        help_text="Run bet2 and then betsurf to get addiotional skull and scalp surfaces (includes registration)",
    )
    # Skipped t2_guided option
    functional = models.BooleanField(default=False, help_text="Apply to 4D fMRI data")
    reduce_bias = models.BooleanField(
        default=False, help_text="Bias field and neck cleanup"
    )

