from django.contrib import admin

from .models import Fotografia


@admin.register(Fotografia)
class FotografiaAdmin(admin.ModelAdmin):
    list_display = ("planta", "data_foto", "imagem")
    list_filter = ("data_foto",)
    search_fields = ("planta__nome_popular", "planta__nome_cientifico")
    autocomplete_fields = ("planta",)
    date_hierarchy = "data_foto"
