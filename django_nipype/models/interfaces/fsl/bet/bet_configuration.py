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

    MUTUALLY_EXCLUSIVE = [
        "robust",
        "padding",
        "remove_eyes",
        "surfaces",
        "functional",
        "reduce_bias",
    ]

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

    class Meta:
        verbose_name_plural = "Configurations"

    def validate_mutually_exclusive(self, **kwargs):
        selected = [kwargs.get(mode, True) for mode in self.MUTUALLY_EXCLUSIVE]
        if sum(selected) > 1:
            return False
        return True

    def save(self, *args, **kwargs):
        if not self.validate_mutually_exclusive(**kwargs):
            raise ValueError(
                f"The following fields are mutually exclusive:\n{self.MUTUALLY_EXCLUSIVE}"
            )
        else:
            super(BetConfiguration, self).save(*args, **kwargs)

    def create_kwargs(self):
        d = model_to_dict(self)
        skip = ["id", "name"] + self.MUTUALLY_EXCLUSIVE
        keys = [
            key
            for key in d.keys()
            if key not in skip or (key in self.MUTUALLY_EXCLUSIVE and d[key])
        ]
        keys = [key for key in keys if d.get(key)]
        return {self.CONFIG_DICT.get(key, key): d[key] for key in keys}
