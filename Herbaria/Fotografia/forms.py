from django import forms

from Plantas.widgets import DateInput

from .models import Fotografia


class FotografiaForm(forms.ModelForm):
    descricao_formulario = "Selecione a planta e envie uma imagem para registrar sua aparência na data da fotografia."
    class Meta:
        model = Fotografia
        fields = ("planta", "imagem", "data_foto")
        labels = {"planta": "Planta fotografada", "imagem": "Arquivo da fotografia", "data_foto": "Data da fotografia"}
        help_texts = {"planta": "Escolha a planta que aparece na imagem.", "imagem": "Selecione um arquivo de imagem, como JPG ou PNG.", "data_foto": "Informe a data em que a fotografia foi tirada."}
        widgets = {"data_foto": DateInput(), "imagem": forms.ClearableFileInput(attrs={"accept": "image/*"})}
        error_messages = {"imagem": {"invalid_image": "Envie um arquivo de imagem válido, como JPG ou PNG."}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["planta"].empty_label = "Selecione a planta fotografada"
