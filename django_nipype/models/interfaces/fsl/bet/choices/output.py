from django_nipype.models.choice_enum import ChoiceEnum


class Output(ChoiceEnum):
    BRN = "Brain"
    SRF = "Surface Outline"
    MSK = "Mask"
    SKL = "Skull"
    MSH = "Mesh Surface"
