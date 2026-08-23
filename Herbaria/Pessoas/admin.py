from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(UserAdmin):
    list_display = (
        "username",
        "nome",
        "cpf",
        "email",
        "cidade",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "sexo", "estado", "groups")
    search_fields = ("username", "nome", "cpf", "email", "telefone")
    filter_horizontal = ("groups", "user_permissions", "plantas")
    ordering = ("nome", "username")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Dados pessoais",
            {
                "fields": (
                    "nome",
                    "cpf",
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
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Dados da pessoa",
            {
                "classes": ("wide",),
                "fields": ("nome", "cpf", "email"),
            },
        ),
    )
