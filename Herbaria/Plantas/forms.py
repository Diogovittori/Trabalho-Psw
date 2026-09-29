from django import forms

from .models import Planta
from .widgets import DateInput


class PlantaForm(forms.ModelForm):
    descricao_formulario = "Informe os dados da planta. Cuidados e fotografias são cadastrados nas respectivas telas após salvar a planta."
    class Meta:
        model = Planta
        fields = (
            "nome_popular",
            "nome_cientifico",
            "descricao",
            "data_plantio",
            "categoria",
        )
        labels = {"nome_popular": "Nome popular", "nome_cientifico": "Nome científico", "descricao": "Descrição da planta", "data_plantio": "Data de plantio", "categoria": "Categoria"}
        help_texts = {
            "nome_popular": "Nome pelo qual a planta é conhecida no dia a dia.",
            "nome_cientifico": "Nome usado para identificar a espécie.",
            "descricao": "Descreva as características da planta. Se necessário, inclua informações sobre ambiente e propriedades neste texto.",
            "data_plantio": "Informe a data em que a planta foi plantada, se souber.",
            "categoria": "Escolha uma categoria já cadastrada para organizar a planta.",
        }
        widgets = {
            "data_plantio": DateInput(),
            "nome_popular": forms.TextInput(attrs={"placeholder": "Ex.: Hortelã"}),
            "nome_cientifico": forms.TextInput(attrs={"placeholder": "Ex.: Mentha spicata"}),
            "descricao": forms.Textarea(attrs={"placeholder": "Descreva a aparência e outras características da planta.", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].empty_label = "Sem categoria"
