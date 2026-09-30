from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Coalesce, NullIf
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from .acesso import proprietario_required, eh_funcionario
from .forms import PessoaEdicaoForm
from .models import Pessoa


@proprietario_required("view")
@require_safe
def pessoa_listar(request):
    usuarios = User.objects.annotate(nome=Coalesce(NullIf("pessoa__nome", Value("")), NullIf("first_name", Value("")), "username")).order_by("nome", "pk")
    pagina = Paginator(usuarios, 20).get_page(request.GET.get("page"))
    return render(request, "Pessoas/administracao/listar.html", {"pagina": pagina})


@proprietario_required("view")
@require_safe
def pessoa_detalhar(request, pk):
    usuario = get_object_or_404(User.objects.select_related("pessoa"), pk=pk)
    pessoa = getattr(usuario, "pessoa", usuario)
    return render(request, "Pessoas/administracao/detalhar.html", {"pessoa": pessoa, "funcionario": eh_funcionario(usuario)})


@proprietario_required("change")
@require_http_methods(["GET", "POST"])
def pessoa_editar(request, pk):
    usuario = get_object_or_404(User.objects.select_related("pessoa"), pk=pk)
    pessoa = getattr(usuario, "pessoa", None)
    if pessoa is None:
        # Completa o perfil sem recriar a conta ou substituir senha e privilégios.
        dados_usuario = {campo.attname: getattr(usuario, campo.attname) for campo in User._meta.concrete_fields}
        pessoa = Pessoa(user_ptr=usuario, nome=usuario.get_full_name(), **dados_usuario)
        pessoa._state.adding = False
        pessoa._state.db = usuario._state.db
    form = PessoaEdicaoForm(request.POST if request.method == "POST" else None, instance=pessoa)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            form.add_error(None, "Não foi possível salvar. Confira se o nome de usuário ou CPF já está cadastrado.")
        else:
            messages.success(request, "Pessoa atualizada com sucesso.")
            return redirect("pessoas:pessoa_listar")
    return render(request, "Pessoas/administracao/editar.html", {"form": form, "pessoa": pessoa})


@proprietario_required("delete")
@require_http_methods(["GET", "POST"])
def pessoa_excluir(request, pk):
    pessoa = get_object_or_404(User, pk=pk)
    if pessoa.pk == request.user.pk:
        messages.error(request, "Você não pode excluir a própria conta por esta área.")
        return redirect("pessoas:pessoa_listar")
    if request.method == "POST":
        try:
            with transaction.atomic():
                pessoa.delete()
        except ProtectedError:
            messages.error(request, "Esta pessoa possui registros protegidos e não pode ser excluída.")
        else:
            messages.success(request, "Pessoa excluída com sucesso.")
            return redirect("pessoas:pessoa_listar")
    return render(request, "Pessoas/administracao/excluir.html", {"pessoa": pessoa})
