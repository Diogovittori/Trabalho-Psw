from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FotografiaForm
from .models import Fotografia


def fotografia_listar(request):
    fotografias = Fotografia.objects.select_related("planta")
    return render(
        request, "Plantas/fotografia_listar.html", {"fotografias": fotografias}
    )


def fotografia_criar(request):
    if request.method == "POST":
        form = FotografiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Fotografia cadastrada com sucesso.")
            return redirect("plantas:fotografia_listar")
    else:
        form = FotografiaForm()
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
    if request.method == "POST":
        form = FotografiaForm(
            request.POST, request.FILES, instance=fotografia
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Fotografia atualizada com sucesso.")
            return redirect("plantas:fotografia_listar")
    else:
        form = FotografiaForm(instance=fotografia)
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
