from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm, CuidadosForm, FotografiaForm, PlantaForm
from Categoria.models import Categoria
from Cuidados.models import Cuidados
from Fotografia.models import Fotografia
from .models import Planta


def inicio(request):
    return redirect("plantas:planta_listar")


def categoria_listar(request):
    categorias = Categoria.objects.prefetch_related("plantas")
    return render(
        request, "Plantas/categoria_listar.html", {"categorias": categorias}
    )


def categoria_criar(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Categoria cadastrada com sucesso.")
        return redirect("plantas:categoria_listar")
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
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        messages.success(request, "Categoria atualizada com sucesso.")
        return redirect("plantas:categoria_listar")
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


def planta_listar(request):
    plantas = Planta.objects.select_related("categoria")
    return render(request, "Plantas/planta_listar.html", {"plantas": plantas})


def planta_criar(request):
    form = PlantaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Planta cadastrada com sucesso.")
        return redirect("plantas:planta_listar")
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Cadastrar planta"},
    )


def planta_detalhar(request, pk):
    planta = get_object_or_404(
        Planta.objects.select_related("categoria").prefetch_related(
            "cuidados", "fotografias"
        ),
        pk=pk,
    )
    return render(request, "Plantas/planta_detalhar.html", {"planta": planta})


def planta_editar(request, pk):
    planta = get_object_or_404(Planta, pk=pk)
    form = PlantaForm(request.POST or None, instance=planta)
    if form.is_valid():
        form.save()
        messages.success(request, "Planta atualizada com sucesso.")
        return redirect("plantas:planta_listar")
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Editar planta"},
    )


def planta_excluir(request, pk):
    planta = get_object_or_404(Planta, pk=pk)
    if request.method == "POST":
        planta.delete()
        messages.success(request, "Planta excluída com sucesso.")
        return redirect("plantas:planta_listar")
    return render(
        request,
        "Plantas/confirmar_exclusao.html",
        {"objeto": planta, "tipo": "planta"},
    )


def cuidado_listar(request):
    cuidados = Cuidados.objects.select_related("planta")
    return render(request, "Plantas/cuidado_listar.html", {"cuidados": cuidados})


def cuidado_criar(request):
    form = CuidadosForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Cuidado cadastrado com sucesso.")
        return redirect("plantas:cuidado_listar")
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Cadastrar cuidado"},
    )


def cuidado_detalhar(request, pk):
    cuidado = get_object_or_404(Cuidados.objects.select_related("planta"), pk=pk)
    return render(
        request, "Plantas/cuidado_detalhar.html", {"cuidado": cuidado}
    )


def cuidado_editar(request, pk):
    cuidado = get_object_or_404(Cuidados, pk=pk)
    form = CuidadosForm(request.POST or None, instance=cuidado)
    if form.is_valid():
        form.save()
        messages.success(request, "Cuidado atualizado com sucesso.")
        return redirect("plantas:cuidado_listar")
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Editar cuidado"},
    )


def cuidado_excluir(request, pk):
    cuidado = get_object_or_404(Cuidados, pk=pk)
    if request.method == "POST":
        cuidado.delete()
        messages.success(request, "Cuidado excluído com sucesso.")
        return redirect("plantas:cuidado_listar")
    return render(
        request,
        "Plantas/confirmar_exclusao.html",
        {"objeto": cuidado, "tipo": "cuidado"},
    )


def fotografia_listar(request):
    fotografias = Fotografia.objects.select_related("planta")
    return render(
        request, "Plantas/fotografia_listar.html", {"fotografias": fotografias}
    )


def fotografia_criar(request):
    form = FotografiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Fotografia cadastrada com sucesso.")
        return redirect("plantas:fotografia_listar")
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Cadastrar fotografia", "multipart": True},
    )


def fotografia_detalhar(request, pk):
    fotografia = get_object_or_404(
        Fotografia.objects.select_related("planta"), pk=pk
    )
    return render(
        request, "Plantas/fotografia_detalhar.html", {"fotografia": fotografia}
    )


def fotografia_editar(request, pk):
    fotografia = get_object_or_404(Fotografia, pk=pk)
    form = FotografiaForm(
        request.POST or None, request.FILES or None, instance=fotografia
    )
    if form.is_valid():
        form.save()
        messages.success(request, "Fotografia atualizada com sucesso.")
        return redirect("plantas:fotografia_listar")
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Editar fotografia", "multipart": True},
    )


def fotografia_excluir(request, pk):
    fotografia = get_object_or_404(Fotografia, pk=pk)
    if request.method == "POST":
        fotografia.delete()
        messages.success(request, "Fotografia excluída com sucesso.")
        return redirect("plantas:fotografia_listar")
    return render(
        request,
        "Plantas/confirmar_exclusao.html",
        {"objeto": fotografia, "tipo": "fotografia"},
    )
