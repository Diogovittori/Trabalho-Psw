from django.contrib import admin

from .models import Categoria, Cuidados, Fotografia, Planta


class CuidadosInline(admin.TabularInline):
    model = Cuidados
    extra = 0


class FotografiaInline(admin.TabularInline):
    model = Fotografia
    extra = 0


@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = (
        "nome_popular",
        "nome_cientifico",
        "categoria",
        "status",
        "data_plantio",
        "data_cadastro",
    )
    list_filter = ("status", "categoria", "data_cadastro", "data_plantio")
    search_fields = ("nome_popular", "nome_cientifico", "descricao")
    autocomplete_fields = ("categoria",)
    date_hierarchy = "data_cadastro"
    inlines = (CuidadosInline, FotografiaInline)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome", "descricao")


@admin.register(Cuidados)
class CuidadosAdmin(admin.ModelAdmin):
    list_display = ("planta", "tipo", "data")
    list_filter = ("tipo", "data")
    search_fields = ("planta__nome_popular", "observacoes")
    autocomplete_fields = ("planta",)
    date_hierarchy = "data"


@admin.register(Fotografia)
class FotografiaAdmin(admin.ModelAdmin):
    list_display = ("planta", "data_foto", "imagem")
    list_filter = ("data_foto",)
    search_fields = ("planta__nome_popular", "planta__nome_cientifico")
    autocomplete_fields = ("planta",)
    date_hierarchy = "data_foto"
