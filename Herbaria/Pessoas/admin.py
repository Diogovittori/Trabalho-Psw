from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(UserAdmin):
    list_display = ("username", "nome", "cpf", "email", "cidade")
    list_filter = ("sexo", "estado")
    search_fields = (
        "username",
        "nome",
        "email",
        "cpf",
        "telefone",
    )
    filter_horizontal = ("groups", "user_permissions", "plantas")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Dados pessoais",
            {
                "fields": (
                    "cpf",
                    "nome",
                    "data_nascimento",
                    "sexo",
                    "telefone",
                )
            },
        ),
        (
            "Endereço",
            {"fields": ("numero", "bairro", "cidade", "estado", "cep")},
        ),
        ("Herbário", {"fields": ("plantas",)}),
    )
