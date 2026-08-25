from django.urls import path

from Categoria import views as categoria_views
from Cuidados import views as cuidado_views
from Fotografia import views as fotografia_views
from . import views

app_name = "plantas"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("categorias/", categoria_views.categoria_listar, name="categoria_listar"),
    path("categorias/nova/", categoria_views.categoria_criar, name="categoria_criar"),
    path("categorias/<int:pk>/", categoria_views.categoria_detalhar, name="categoria_detalhar"),
    path("categorias/<int:pk>/editar/", categoria_views.categoria_editar, name="categoria_editar"),
    path("categorias/<int:pk>/excluir/", categoria_views.categoria_excluir, name="categoria_excluir"),
    path("plantas/", views.planta_listar, name="planta_listar"),
    path("plantas/nova/", views.planta_criar, name="planta_criar"),
    path("plantas/<int:pk>/", views.planta_detalhar, name="planta_detalhar"),
    path("plantas/<int:pk>/editar/", views.planta_editar, name="planta_editar"),
    path("plantas/<int:pk>/excluir/", views.planta_excluir, name="planta_excluir"),
    path("cuidados/", cuidado_views.cuidado_listar, name="cuidado_listar"),
    path("cuidados/novo/", cuidado_views.cuidado_criar, name="cuidado_criar"),
    path("cuidados/<int:pk>/", cuidado_views.cuidado_detalhar, name="cuidado_detalhar"),
    path("cuidados/<int:pk>/editar/", cuidado_views.cuidado_editar, name="cuidado_editar"),
    path("cuidados/<int:pk>/excluir/", cuidado_views.cuidado_excluir, name="cuidado_excluir"),
    path("fotografias/", fotografia_views.fotografia_listar, name="fotografia_listar"),
    path("fotografias/nova/", fotografia_views.fotografia_criar, name="fotografia_criar"),
    path("fotografias/<int:pk>/", fotografia_views.fotografia_detalhar, name="fotografia_detalhar"),
    path("fotografias/<int:pk>/editar/", fotografia_views.fotografia_editar, name="fotografia_editar"),
    path("fotografias/<int:pk>/excluir/", fotografia_views.fotografia_excluir, name="fotografia_excluir"),
]
