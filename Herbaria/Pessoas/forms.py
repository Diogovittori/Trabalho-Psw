import re

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Value
from django.db.models.functions import Replace

from .models import Pessoa, validar_cpf


class OpcoesCadastroPessoa(UserCreationForm.Meta):
    model = Pessoa
    fields = ("username", "email", "nome", "cpf")


class PessoaCadastroForm(UserCreationForm):
    Meta = OpcoesCadastroPessoa
    email = forms.EmailField(label="E-mail", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        textos = {
            "username": ("Nome de usuário", "Ex.: ana.silva", "username"),
            "email": ("E-mail", "Ex.: ana@exemplo.com", "email"),
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
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_cpf(self):
        valor = self.cleaned_data["cpf"].strip()
        if not re.fullmatch(r"(?:[0-9]{11}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2})", valor):
            raise forms.ValidationError("Use 11 dígitos ou o formato 000.000.000-00.")
        cpf = valor.replace(".", "").replace("-", "")
        validar_cpf(cpf)
        existentes = Pessoa.objects.annotate(
            cpf_sem_mascara=Replace(
                Replace(Replace("cpf", Value("."), Value("")), Value("-"), Value("")),
                Value(" "), Value(""),
            )
        )
        if existentes.filter(cpf_sem_mascara=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf


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
