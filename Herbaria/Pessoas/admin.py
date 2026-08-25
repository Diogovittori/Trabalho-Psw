from django.contrib import admin

from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "nome", "cpf", "email", "cidade")
    list_filter = ("sexo", "estado")
    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
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

    @admin.display(description="nome", ordering="usuario__first_name")
    def nome(self, pessoa):
        return pessoa.usuario.get_full_name()

    @admin.display(description="e-mail", ordering="usuario__email")
    def email(self, pessoa):
        return pessoa.usuario.email
