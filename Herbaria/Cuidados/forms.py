from django import forms

from Plantas.widgets import DateInput

from .models import Cuidados, TipoDeCuidado


class CuidadosForm(forms.ModelForm):
    descricao_formulario = "Selecione a planta, os tipos de cuidado e a data do cuidado."
    tipo = forms.ModelMultipleChoiceField(
        queryset=TipoDeCuidado.objects.all(),
        label="Tipos de cuidado",
        widget=forms.CheckboxSelectMultiple,
        help_text="Marque um ou mais cuidados.",
    )

    class Meta:
        model = Cuidados
        fields = ("planta", "tipo", "data", "observacoes")
        labels = {"planta": "Planta", "data": "Data do cuidado", "observacoes": "Observações"}
        help_texts = {"planta": "Escolha a planta à qual este cuidado se refere.", "data": "Informe a data em que o cuidado foi ou será realizado.", "observacoes": "Acrescente detalhes sobre o cuidado, se necessário."}
        widgets = {"data": DateInput(), "observacoes": forms.Textarea(attrs={"placeholder": "Ex.: Regar pela manhã, sem encharcar o solo.", "rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["planta"].empty_label = "Selecione a planta"
