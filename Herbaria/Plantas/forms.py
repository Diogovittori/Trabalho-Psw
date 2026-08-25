from django import forms

from .models import Planta


class DateInput(forms.DateInput):
    input_type = "date"


class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = (
            "nome_cientifico",
            "nome_popular",
            "descricao",
            "data_plantio",
            "categoria",
        )
        widgets = {"data_plantio": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].empty_label = "Selecione uma opção"
