from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from Plantas.forms import CategoriaForm
from .models import Categoria


def categoria_listar(request):
    categorias = Categoria.objects.prefetch_related("plantas")
    return render(
        request, "Plantas/categoria_listar.html", {"categorias": categorias}
    )


def categoria_criar(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria cadastrada com sucesso.")
            return redirect("plantas:categoria_listar")
    else:
        form = CategoriaForm()
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Cadastrar categoria"},
    )


def categoria_detalhar(request, pk):
    categoria = get_object_or_404(
        Categoria.objects.prefetch_related("plantas"), pk=pk
    )
    return render(
        request, "Plantas/categoria_detalhar.html", {"categoria": categoria}
    )


def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso.")
            return redirect("plantas:categoria_listar")
    else:
        form = CategoriaForm(instance=categoria)
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Editar categoria"},
    )


def categoria_excluir(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        categoria.delete()
        messages.success(request, "Categoria excluída com sucesso.")
        return redirect("plantas:categoria_listar")
    return render(
        request,
        "Plantas/confirmar_exclusao.html",
        {"objeto": categoria, "tipo": "categoria"},
    )
