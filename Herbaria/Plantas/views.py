from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PlantaForm
from .models import Planta
from .pesquisa import contexto_listagem, filtrar, termo_pesquisa


@login_required
def inicio(request):
    return redirect("plantas:planta_listar")


@login_required
def planta_listar(request):
    plantas = Planta.objects.select_related("categoria").prefetch_related("fotografias").order_by("nome_popular", "nome_cientifico", "pk")
    return render(request, "Plantas/planta_listar.html", contexto_listagem(request, plantas, "plantas"))


@login_required
def pesquisar(request):
    from Categoria.models import Categoria
    from Cuidados.models import Cuidados
    from Fotografia.models import Fotografia

    termo = termo_pesquisa(request)
    grupos = []
    fontes = (
        ("plantas", "Plantas", "planta", Planta.objects.select_related("categoria").prefetch_related("fotografias").order_by("nome_popular", "pk")),
        ("fotografias", "Fotografias", "fotografia", Fotografia.objects.select_related("planta", "planta__categoria").order_by("-data_foto", "-pk")),
        ("cuidados", "Cuidados", "cuidado", Cuidados.objects.select_related("planta").prefetch_related("tipo").order_by("-data", "-pk")),
        ("categorias", "Categorias", "categoria", Categoria.objects.order_by("nome", "pk")),
    )
    if termo:
        for entidade, titulo, rota, queryset in fontes:
            resultados = filtrar(queryset, entidade, termo)
            grupos.append({"entidade": entidade, "titulo": titulo, "rota": rota,
                           "total": resultados.count(), "objetos": resultados[:6]})
    return render(request, "Plantas/pesquisa.html", {
        "q": termo, "grupos": grupos, "total": sum(grupo["total"] for grupo in grupos),
    })


@login_required
@permission_required("plantas.add_planta", raise_exception=True)
def planta_criar(request):
    if request.method == "POST":
        form = PlantaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Planta cadastrada com sucesso.")
            return redirect("plantas:planta_listar")
    else:
        form = PlantaForm()
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Cadastrar planta"},
    )


@login_required
def planta_detalhar(request, pk):
    planta = get_object_or_404(
        Planta.objects.select_related("categoria").prefetch_related(
            "cuidados__tipo", "fotografias"
        ),
        pk=pk,
    )
    return render(request, "Plantas/planta_detalhar.html", {"planta": planta})


@login_required
@permission_required("plantas.change_planta", raise_exception=True)
def planta_editar(request, pk):
    planta = get_object_or_404(Planta, pk=pk)
    if request.method == "POST":
        form = PlantaForm(request.POST, instance=planta)
        if form.is_valid():
            form.save()
            messages.success(request, "Planta atualizada com sucesso.")
            return redirect("plantas:planta_listar")
    else:
        form = PlantaForm(instance=planta)
    return render(
        request,
        "Plantas/formulario.html",
        {"form": form, "titulo": "Editar planta"},
    )


@login_required
@permission_required("plantas.delete_planta", raise_exception=True)
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


