from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import PessoaCadastroForm

from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(UserAdmin):
    add_form = PessoaCadastroForm
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": (
            "username", "email", "nome", "cpf", "password1", "password2",
        )}),
    )

    list_display = ("username", "nome", "cpf", "email", "cidade")
    list_filter = ("estado",)
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
