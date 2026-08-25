from django.contrib import admin

from Cuidados.models import Cuidado as Cuidados
from Fotografia.models import Fotografia

from .models import Planta


class CuidadosInline(admin.TabularInline):
    model = Cuidados
    extra = 0


class FotografiaInline(admin.TabularInline):
    model = Fotografia
    extra = 0


@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = (
        "nome_popular", "nome_cientifico", "categoria",
        "data_plantio", "data_cadastro",
    )
    list_filter = ("categoria", "data_cadastro", "data_plantio")
    search_fields = ("nome_popular", "nome_cientifico", "descricao")
    autocomplete_fields = ("categoria",)
    date_hierarchy = "data_cadastro"
    inlines = (CuidadosInline, FotografiaInline)
