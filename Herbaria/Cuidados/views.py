from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CuidadosForm
from .models import Cuidados


@login_required
def cuidado_listar(request):
    cuidado = Cuidados.objects.select_related("planta")
    return render(request, "Plantas/cuidado_listar.html", {"cuidado": cuidado})


@permission_required("cuidados.add_cuidados", raise_exception=True)
def cuidado_criar(request):
    if request.method == "POST":
        form = CuidadosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuidado cadastrado com sucesso.")
            return redirect("plantas:cuidado_listar")
    else:
        form = CuidadosForm()
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Cadastrar cuidado"},
    )


@login_required
def cuidado_detalhar(request, pk):
    cuidado = get_object_or_404(Cuidados.objects.select_related("planta"), pk=pk)
    return render(
        request, "Plantas/cuidado_detalhar.html", {"cuidado": cuidado}
    )


@permission_required("cuidados.change_cuidados", raise_exception=True)
def cuidado_editar(request, pk):
    cuidado = get_object_or_404(Cuidados, pk=pk)
    if request.method == "POST":
        form = CuidadosForm(request.POST, instance=cuidado)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuidado atualizado com sucesso.")
            return redirect("plantas:cuidado_listar")
    else:
        form = CuidadosForm(instance=cuidado)
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Editar cuidado"},
    )


@permission_required("cuidados.delete_cuidados", raise_exception=True)
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
