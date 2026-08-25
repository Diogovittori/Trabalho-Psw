from django.contrib import admin

from .models import Cuidados, TipoDeCuidado


@admin.register(TipoDeCuidado)
class TipoDeCuidadoAdmin(admin.ModelAdmin):
    list_display = ("nome", "codigo")
    search_fields = ("nome", "codigo")


@admin.register(Cuidados)
class CuidadosAdmin(admin.ModelAdmin):
    list_display = ("planta", "get_tipos_display", "data")
    list_filter = ("tipo", "data")
    search_fields = ("planta__nome_popular", "observacoes")
    autocomplete_fields = ("planta",)
    date_hierarchy = "data"
