from django.contrib import admin

from .models import Cuidados


@admin.register(Cuidados)
class CuidadosAdmin(admin.ModelAdmin):
    list_display = ("planta", "tipo", "data")
    list_filter = ("tipo", "data")
    search_fields = ("planta__nome_popular", "observacoes")
    autocomplete_fields = ("planta",)
    date_hierarchy = "data"
