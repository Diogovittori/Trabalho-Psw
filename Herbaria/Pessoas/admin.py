from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(UserAdmin):
    list_display = ("username", "nome", "cpf", "email", "cidade")
    list_filter = ("sexo", "estado")
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "cpf",
        "telefone",
    )
    filter_horizontal = ("groups", "user_permissions", "plantas")
    fieldsets = (
        ("Usuário", {"fields": ("username", "password")} ),
        (
            "Informações pessoais",
            {"fields": ("first_name", "last_name", "email")},
        ),
        (
            "Dados pessoais",
            {
                "fields": (
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
        (
            "Permissões",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "cpf",
                ),
            },
        ),
    )

    @admin.display(description="nome", ordering="first_name")
    def nome(self, pessoa):
        return pessoa.get_full_name()
