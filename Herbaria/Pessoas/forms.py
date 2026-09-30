from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone

from Plantas.widgets import DateInput
from .models import Pessoa
from .validacoes import validar_cpf_disponivel, validar_username_disponivel
from .acesso import eh_funcionario


class OpcoesCadastroPessoa(UserCreationForm.Meta):
    model = Pessoa
    fields = ("username", "email", "nome", "cpf", "data_nascimento", "telefone",
              "numero", "bairro", "cidade", "estado", "cep")
    labels = {"numero": "Número do endereço", "estado": "Estado (UF)", "cep": "CEP"}
    widgets = {"data_nascimento": DateInput(), "telefone": forms.TextInput(attrs={"type": "tel", "placeholder": "Ex.: (11) 99999-9999"})}


class DadosPessoaisMixin:
    def clean_data_nascimento(self):
        data = self.cleaned_data["data_nascimento"]
        if data and data > timezone.localdate():
            raise forms.ValidationError("A data de nascimento não pode estar no futuro.")
        return data

    def clean_estado(self):
        estado = self.cleaned_data["estado"].upper()
        if estado and estado not in "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split():
            raise forms.ValidationError("Informe uma sigla de estado válida, como SP.")
        return estado


class PessoaCadastroForm(DadosPessoaisMixin, UserCreationForm):
    Meta = OpcoesCadastroPessoa
    email = forms.EmailField(label="E-mail", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_nascimento"].required = True
        self.fields["telefone"].required = True
        textos = {
            "username": ("Nome de usuário", "Ex.: fulado", "username"),
            "email": ("E-mail", "Ex.: exemplo@exemplo.com", "email"),
            "nome": ("Nome completo", "Digite seu nome completo", "name"),
            "cpf": ("CPF", "000.000.000-00", "off"),
            "password1": ("Senha", "Crie uma senha", "new-password"),
            "password2": ("Confirmar senha", "Repita a senha", "new-password"),
        }
        for nome, (label, placeholder, autocomplete) in textos.items():
            self.fields[nome].label = label
            self.fields[nome].widget.attrs.update(placeholder=placeholder, autocomplete=autocomplete)
        self.fields["username"].help_text = "Use este nome para entrar no sistema. Até 150 caracteres: letras, números e @/./+/-/_."
        self.fields["cpf"].help_text = "Informe 11 dígitos, com ou sem pontos e traço."
        self.fields["password2"].help_text = "Digite a mesma senha para confirmar."

    def clean_username(self):
        return validar_username_disponivel(self.cleaned_data["username"], self.instance.pk)

    def clean_cpf(self):
        return validar_cpf_disponivel(self.cleaned_data["cpf"], self.instance.pk)


class PessoaEdicaoForm(DadosPessoaisMixin, forms.ModelForm):
    email = forms.EmailField(label="E-mail", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk or not eh_funcionario(self.instance):
            self.fields.pop("plantas")

    class Meta:
        model = Pessoa
        fields = ("username", "nome", "email", "cpf", "data_nascimento", "telefone",
                  "numero", "bairro", "cidade", "estado", "cep", "plantas")
        labels = {"username": "Nome de usuário", "nome": "Nome completo", "cpf": "CPF",
                  "numero": "Número do endereço", "estado": "Estado (UF)", "cep": "CEP",
                  "plantas": "Plantas vinculadas"}
        widgets = {"data_nascimento": DateInput(), "estado": forms.TextInput(attrs={"placeholder": "Ex.: SP"})}
        help_texts = {"cpf": "Informe 11 dígitos, com ou sem pontos e traço.",
                      "cep": "Informe apenas os números do CEP.",
                      "plantas": "Use Ctrl (ou Command no Mac) para selecionar mais de uma planta."}

    def clean_username(self):
        return validar_username_disponivel(self.cleaned_data["username"], self.instance.pk)

    def clean_cpf(self):
        return validar_cpf_disponivel(self.cleaned_data["cpf"], self.instance.pk)

class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Nome de usuário ou senha incorretos. Confira os dados e tente novamente.",
        "inactive": "Esta conta está inativa. Entre em contato com a administração do sistema.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nome de usuário"
        self.fields["username"].widget.attrs.update(placeholder="Digite seu nome de usuário", autocomplete="username")
        self.fields["password"].label = "Senha"
        self.fields["password"].widget.attrs.update(placeholder="Digite sua senha", autocomplete="current-password")
