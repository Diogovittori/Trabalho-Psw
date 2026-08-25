from django.contrib import admin

from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "nome", "cpf", "email", "cidade")
    list_filter = ("sexo", "estado")
    search_fields = (
        "usuario__username",
        "nome",
        "email",
        "cpf",
        "telefone",
    )
    autocomplete_fields = ("usuario",)
    filter_horizontal = ("plantas",)
    fieldsets = (
        ("Usuário", {"fields": ("usuario",)}),
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
