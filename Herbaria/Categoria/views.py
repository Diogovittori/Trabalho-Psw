from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm
from .models import Categoria


@login_required
def categoria_listar(request):
    categorias = Categoria.objects.prefetch_related("plantas")
    return render(
        request, "Plantas/categoria_listar.html", {"categorias": categorias}
    )


@login_required
@permission_required("categoria.add_categoria", raise_exception=True)
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


@login_required
def categoria_detalhar(request, pk):
    categoria = get_object_or_404(
        Categoria.objects.prefetch_related("plantas"), pk=pk
    )
    return render(
        request, "Plantas/categoria_detalhar.html", {"categoria": categoria}
    )


@login_required
@permission_required("categoria.change_categoria", raise_exception=True)
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


@login_required
@permission_required("categoria.delete_categoria", raise_exception=True)
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
