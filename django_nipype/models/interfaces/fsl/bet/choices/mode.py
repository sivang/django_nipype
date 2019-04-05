from django_nipype.models.choice_enum import ChoiceEnum


class Mode(ChoiceEnum):
    NORMAL = "Normal"
    ROBUST = "Robust"
    PADDNG = "Padding"
    REMOVE = "Remove Eyes"
    SURFAC = "Surfaces"
    FUNCTN = "Funational"
    REDUBI = "Reduce Bias"
