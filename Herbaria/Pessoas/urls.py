from django.urls import path

from . import views_administracao as views

app_name = "pessoas"

urlpatterns = [
    path("administracao/", views.pessoa_listar, name="pessoa_listar"),
    path("administracao/<int:pk>/", views.pessoa_detalhar, name="pessoa_detalhar"),
    path("administracao/<int:pk>/editar/", views.pessoa_editar, name="pessoa_editar"),
    path("administracao/<int:pk>/excluir/", views.pessoa_excluir, name="pessoa_excluir"),
]
