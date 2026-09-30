import re

from django import forms
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Replace

from .models import Pessoa, validar_cpf


def validar_username_disponivel(username, pessoa_pk=None):
    if User.objects.filter(username__iexact=username).exclude(pk=pessoa_pk).exists():
        raise forms.ValidationError("Este nome de usuário já está em uso.")
    return username


def validar_cpf_disponivel(valor, pessoa_pk=None):
    valor = valor.strip()
    if not re.fullmatch(r"(?:[0-9]{11}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2})", valor):
        raise forms.ValidationError("Use 11 dígitos ou o formato 000.000.000-00.")
    cpf = valor.replace(".", "").replace("-", "")
    validar_cpf(cpf)
    existentes = Pessoa.objects.exclude(pk=pessoa_pk).annotate(
        cpf_sem_mascara=Replace(
            Replace(Replace("cpf", Value("."), Value("")), Value("-"), Value("")),
            Value(" "), Value(""),
        )
    )
    if existentes.filter(cpf_sem_mascara=cpf).exists():
        raise forms.ValidationError("Este CPF já está cadastrado.")
    return cpf
