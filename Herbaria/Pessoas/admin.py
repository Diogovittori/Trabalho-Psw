from django.contrib import admin

from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ("username", "nome", "cpf", "email", "cidade")
    list_filter = ("sexo", "estado")
    search_fields = (
        "username",
        "nome",
        "email",
        "cpf",
        "telefone",
    )
    filter_horizontal = ("plantas",)
    fieldsets = (
        ("Usuário", {"fields": ("username",)}),
        (
            "Dados pessoais",
            {
                "fields": (
                    "cpf",
                    "nome",
                    "data_nascimento",
                    "sexo",
                    "email",
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
