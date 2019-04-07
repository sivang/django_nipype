from django.db import models
from django_nipype.models.interfaces.fsl.bet.choices import Output
from django_nipype.models.vertex import VertexFileOutput


class BetOutput(VertexFileOutput):
    output_type = models.CharField(max_length=3, choices=Output.choices())
    run = models.ForeignKey(
        "django_nipype.BetRun", on_delete=models.CASCADE, related_name="output_set"
    )

    SUFFIX = {
        Output.MSH.name: "_mesh",
        Output.MSK.name: "_mask",
        Output.OUT.name: "_overlay",
        Output.SRF.name: [
            "_inskull_mask",
            "_inskull_mesh",
            "_outskull_mask",
            "_outskull_mesh",
            "_outskin_mask",
            "_outskin_mesh",
            "_skull_mask",
        ],
    }
    DEFAULT_EXTENSION = "nii.gz"
    EXTENSION = {Output.MSH.name: "vtk"}
    INTERFACE_CONFIGURATION_KEYS = {
        Output.BRN.name: "out_file",
        Output.MSH.name: "mesh",
        Output.MSK.name: "mask",
        Output.OUT.name: "outline",
        Output.SRF.name: "surfaces",
    }
    SHORT_DESCRIPTIONS = {choice.name: choice.value for choice in Output}

    def get_interface_configuration(self) -> dict:
        if self.output_type == Output.BRN.name:
            return {self.INTERFACE_CONFIGURATION_KEYS.get(self.output_type): self.path}
        return super().get_interface_configuration()
