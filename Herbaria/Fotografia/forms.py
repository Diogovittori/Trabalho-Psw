from django import forms

from .models import Fotografia


class DateInput(forms.DateInput):
    input_type = "date"


class FotografiaForm(forms.ModelForm):
    class Meta:
        model = Fotografia
        fields = ("planta", "imagem", "data_foto")
        widgets = {"data_foto": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["planta"].empty_label = "Selecione uma opção"
