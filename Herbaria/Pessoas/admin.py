from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import PessoaCadastroForm

from .models import Pessoa
from .acesso import eh_funcionario


@admin.register(Pessoa)
class PessoaAdmin(UserAdmin):
    add_form = PessoaCadastroForm
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": (
            "username", "email", "nome", "cpf", "password1", "password2",
            "data_nascimento", "telefone", "numero", "bairro", "cidade", "estado", "cep",
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

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None or not eh_funcionario(obj):
            return tuple((titulo, opcoes) for titulo, opcoes in fieldsets if titulo != "Herbário")
        return fieldsets
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
