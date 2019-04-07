from django_nipype.models.choice_enum import ChoiceEnum


class Output(ChoiceEnum):
    BRN = "Brain"
    OUT = "Surface Outline"
    SRF = "Surfaces"
    MSK = "Mask"
    MSH = "Mesh Surface"
