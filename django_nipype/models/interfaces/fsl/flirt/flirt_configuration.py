import json

from django.db import models
from django.forms.models import model_to_dict
from django_nipype.models import NodeConfiguration


class FlirtConfiguration(NodeConfiguration):

    CONFIG_DICT = {
        "interpolation": "interp",
        "cost_function": "cost",
        "degrees_of_freedom": "dof",
        "intensity_clamping": "no_clamp",
        "resample_blur": "no_resample_blur",
        "log": "save_log",
    }

    # Interpolation
    TRILINEAR = "TL"
    NEAREST_NEIGHBOR = "NN"
    SINC = "SI"
    SPLINE = "SP"
    INTERPOLATION_CHOICES = (
        (TRILINEAR, "Trilinear"),
        (NEAREST_NEIGHBOR, "Nearest Neighbor"),
        (SPLINE, "Spline"),
        (SINC, "Sinc"),
    )
    INTERPOLATION_CHOICES_DICT = {
        TRILINEAR: "trilinear",
        NEAREST_NEIGHBOR: "nearestneighbour",
        SINC: "sinc",
        SPLINE: "spline",
    }
    interpolation = models.CharField(
        max_length=2, choices=INTERPOLATION_CHOICES, default=TRILINEAR
    )

    # Cost function
    MUTUAL_INFORMATION = "MUT"
    CORRELATION_RATIO = "COR"
    NORMALIZED_CORRELATION = "NCO"
    NORMALIZED_MUTUAL_INFORMATION = "NMU"
    LEAST_SQUARES = "LSQ"
    LABEL_DIFFERENCE = "LBL"
    BOUNDARY_BASED = "BBR"
    COST_FUNCTION_CHOICES = (
        (MUTUAL_INFORMATION, "Mutual Information"),
        (CORRELATION_RATIO, "Correlation Ratio"),
        (NORMALIZED_CORRELATION, "Normalized Correlation"),
        (NORMALIZED_MUTUAL_INFORMATION, "Normalized Mutual Information"),
        (LEAST_SQUARES, "Least Squares"),
        (LABEL_DIFFERENCE, "Label Difference"),
        (BOUNDARY_BASED, "Boundary-Based Registration"),
    )
    COST_FUNCION_CHOICES_DICT = {
        MUTUAL_INFORMATION: "mutualinfo",
        CORRELATION_RATIO: "corratio",
        NORMALIZED_CORRELATION: "normcorr",
        NORMALIZED_MUTUAL_INFORMATION: "normmi",
        LEAST_SQUARES: "leastsq",
        LABEL_DIFFERENCE: "labeldiff",
        BOUNDARY_BASED: "bbr",
    }
    cost_function = models.CharField(
        max_length=3, choices=COST_FUNCTION_CHOICES, default=CORRELATION_RATIO
    )

    bins = models.PositiveIntegerField(default=256)
    degrees_of_freedom = models.PositiveIntegerField(default=12)

    intensity_clamping = models.BooleanField(default=True)
    resample_blur = models.BooleanField(default=True)
    log = models.BooleanField(default=True)
    # Many more FLIRT and specifically BBR fields to add
    # BBR might even be better off as a subclass

    class Meta:
        verbose_name_plural = "FLIRT Configurations"

    def __str__(self):
        return json.dumps(self.create_kwargs(), indent=2)

    def raw_dict(self) -> dict:
        d = model_to_dict(self)
        skip = ["id", "name", "intensity_clamping", "resample_blur"]
        config = {
            self.CONFIG_DICT.get(key, key): value
            for key, value in d.items()
            if key not in skip and value
        }
        return config

    def add_inverted_boolean_flags(self, config: dict):
        inverted_booleans = ["intensity_clamping", "resample_blur"]
        for flag in inverted_booleans:
            if not getattr(self, flag):
                config[self.CONFIG_DICT.get(flag, flag)] = True
        return config

    def fix_interpolation_kwarg(self, config: dict):
        attribute = self.CONFIG_DICT["interpolation"]
        value = self.INTERPOLATION_CHOICES_DICT[self.interpolation]
        config[attribute] = value
        return config

    def fix_cost_function_kwarg(self, config: dict):
        attribute = self.CONFIG_DICT["cost_function"]
        value = self.COST_FUNCION_CHOICES_DICT[self.cost_function]
        config[attribute] = value
        return config

    def create_kwargs(self):
        config = self.raw_dict()
        config = self.add_inverted_boolean_flags(config)
        config = self.fix_interpolation_kwarg(config)
        config = self.fix_cost_function_kwarg(config)
        return config

