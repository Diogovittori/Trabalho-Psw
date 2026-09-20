import re

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Value
from django.db.models.functions import Replace

from .models import Pessoa, validar_cpf


class OpcoesCadastroPessoa(UserCreationForm.Meta):
    model = Pessoa
    fields = ("username", "email", "nome", "cpf")


class PessoaCadastroForm(UserCreationForm):
    Meta = OpcoesCadastroPessoa
    email = forms.EmailField(label="E-mail", required=True)

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
