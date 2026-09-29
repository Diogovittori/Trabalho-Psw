from django import forms

from .models import Categoria


class CategoriaForm(forms.ModelForm):
    descricao_formulario = "Defina uma categoria para organizar as plantas por características em comum."
    class Meta:
        model = Categoria
        fields = ("nome", "descricao")
        labels = {"nome": "Nome da categoria", "descricao": "Descrição da categoria"}
        help_texts = {"descricao": "Explique quais plantas pertencem a esta categoria."}
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Ornamentais"}),
            "descricao": forms.Textarea(attrs={"placeholder": "Ex.: Plantas cultivadas para decoração.", "rows": 4}),
        }
        error_messages = {"nome": {"unique": "Já existe uma categoria com este nome."}}
