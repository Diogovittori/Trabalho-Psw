from django import forms

from .models import Planta
from .widgets import DateInput


class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = (
            "nome_popular",
            "nome_cientifico",
            "descricao",
            "data_plantio",
            "categoria",
        )
        widgets = {"data_plantio": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].empty_label = "Selecione uma opção"
