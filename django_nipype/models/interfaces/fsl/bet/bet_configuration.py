from django.core.validators import validate_comma_separated_integer_list
from django.db import models, IntegrityError
from django_nipype.models.fields import ChoiceArrayField
from django_nipype.models.interfaces.fsl.bet.bet_run import BetRun
from django_nipype.models.interfaces.fsl.bet.choices import Mode, Output
from django_nipype.models.vertex import VertexConfiguration
from nipype.interfaces.fsl import BET


def default_output() -> list:
    return [Output.BRN.name]


class BetConfiguration(VertexConfiguration):
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
    mode = models.CharField(
        max_length=6, choices=Mode.choices(), default=Mode.NORMAL.name
    )
    base_output_name = models.CharField(max_length=55, blank=True, null=True)
    output = ChoiceArrayField(
        models.CharField(max_length=3, choices=Output.choices()),
        size=5,
        blank=True,
        default=default_output,
    )
    NON_CONFIGURATION_FIELDS = VertexConfiguration.NON_CONFIGURATION_FIELDS + [
        "mode",
        "output",
    ]
    CONFIGURATION_KEYS = {
        "fractional_intensity_threshold": "frac",
        "head_radius": "radius",
        "threshold_segmented": "threshold",
    }
    VALIDATE_DEFAULT_OUTPUT = True

    class Meta:
        verbose_name_plural = "FSL BET Configurations"

    def save(self, *args, **kwargs):
        if self.VALIDATE_DEFAULT_OUTPUT and self.default_in_output:
            super().save(*args, **kwargs)
        else:
            raise IntegrityError(f"Output must contain {default_output()}!")

    def get_mode_kwarg(self) -> str:
        return self.get_mode_display().lower().replace(" ", "_")

    def add_mode_to_kwargs(self, config: dict) -> dict:
        if self.mode != Mode.NORMAL.name:
            kwarg = self.get_mode_kwarg()
            config[kwarg] = True
        return config

    def to_kwargs(self) -> dict:
        config = super().to_kwargs()
        return self.add_mode_to_kwargs(config)

    def create_interface(self) -> BET:
        config = self.to_kwargs()
        return BET(**config)

    def run(self, nifti_path: str) -> BetRun:
        bet = BetRun.objects.create(configuration=self)
        bet.add_input(name="in_file", path=nifti_path)
        return bet.run()

    @property
    def default_in_output(self) -> bool:
        return all([choice in self.output for choice in default_output()])
