from django import forms

from .models import Cuidado, TipoDeCuidado


class DateInput(forms.DateInput):
    input_type = "date"


class CuidadosForm(forms.ModelForm):
    tipo = forms.ModelMultipleChoiceField(
        queryset=TipoDeCuidado.objects.all(),
        label="Tipos de cuidado",
        widget=forms.CheckboxSelectMultiple,
        help_text="Marque um ou mais cuidados.",
    )

    class Meta:
        model = Cuidado
        fields = ("planta", "tipo", "data", "observacoes")
        widgets = {"data": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["planta"].empty_label = "Selecione uma opção"
