from django.urls import path

from . import views

app_name = "plantas"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("categorias/", views.categoria_listar, name="categoria_listar"),
    path("categorias/nova/", views.categoria_criar, name="categoria_criar"),
    path("categorias/<int:pk>/", views.categoria_detalhar, name="categoria_detalhar"),
    path("categorias/<int:pk>/editar/", views.categoria_editar, name="categoria_editar"),
    path("categorias/<int:pk>/excluir/", views.categoria_excluir, name="categoria_excluir"),
    path("plantas/", views.planta_listar, name="planta_listar"),
    path("plantas/nova/", views.planta_criar, name="planta_criar"),
    path("plantas/<int:pk>/", views.planta_detalhar, name="planta_detalhar"),
    path("plantas/<int:pk>/editar/", views.planta_editar, name="planta_editar"),
    path("plantas/<int:pk>/excluir/", views.planta_excluir, name="planta_excluir"),
    path("cuidados/", views.cuidado_listar, name="cuidado_listar"),
    path("cuidados/novo/", views.cuidado_criar, name="cuidado_criar"),
    path("cuidados/<int:pk>/", views.cuidado_detalhar, name="cuidado_detalhar"),
    path("cuidados/<int:pk>/editar/", views.cuidado_editar, name="cuidado_editar"),
    path("cuidados/<int:pk>/excluir/", views.cuidado_excluir, name="cuidado_excluir"),
    path("fotografias/", views.fotografia_listar, name="fotografia_listar"),
    path("fotografias/nova/", views.fotografia_criar, name="fotografia_criar"),
    path("fotografias/<int:pk>/", views.fotografia_detalhar, name="fotografia_detalhar"),
    path("fotografias/<int:pk>/editar/", views.fotografia_editar, name="fotografia_editar"),
    path("fotografias/<int:pk>/excluir/", views.fotografia_excluir, name="fotografia_excluir"),
]
