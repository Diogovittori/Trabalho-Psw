from django import forms

from Categoria.models import Categoria
from Cuidados.models import Cuidados, TipoDeCuidado
from Fotografia.models import Fotografia
from .models import Planta


class DateInput(forms.DateInput):
    input_type = "date"


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ("nome", "descricao")


class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = (
            "nome_cientifico",
            "nome_popular",
            "descricao",
            "status",
            "data_plantio",
            "categoria",
        )
        widgets = {"data_plantio": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].empty_label = "Selecione uma opção"


class CuidadosForm(forms.ModelForm):
    tipo = forms.ModelMultipleChoiceField(
        queryset=TipoDeCuidado.objects.all(),
        label="Tipos de cuidado",
        widget=forms.CheckboxSelectMultiple,
        help_text="Marque um ou mais cuidados.",
    )

    class Meta:
        model = Cuidados
        fields = ("planta", "tipo", "data", "observacoes")
        widgets = {"data": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["planta"].empty_label = "Selecione uma opção"


class FotografiaForm(forms.ModelForm):
    class Meta:
        model = Fotografia
        fields = ("planta", "imagem", "data_foto")
        widgets = {"data_foto": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["planta"].empty_label = "Selecione uma opção"
