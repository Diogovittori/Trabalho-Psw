from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods, require_POST

from .forms import PessoaCadastroForm


@sensitive_post_parameters("password1", "password2")
@csrf_protect
@require_http_methods(["GET", "POST"])
def usuario_cadastrar(request):
    if request.method == "POST":
        form = PessoaCadastroForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    pessoa = form.save()
                    grupo, _ = Group.objects.get_or_create(name="Observadores")
                    pessoa.groups.add(grupo)
            except IntegrityError:
                form.add_error(None, "Não foi possível salvar. Confira se usuário ou CPF já foram cadastrados.")
            else:
                messages.success(request, "Cadastro concluído. Faça login para continuar.")
                return redirect("login")
    else:
        form = PessoaCadastroForm()

    return render(request, "Pessoas/usuario_formulario.html", {
        "form": form,
        "titulo": "Cadastrar usuário",
    })


@sensitive_post_parameters("password")
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):
    next_url = request.POST.get("next", request.GET.get("next", ""))
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = ""

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            # AuthenticationForm já verificou credenciais e usuário ativo.
            login(request, form.get_user())
            return redirect(next_url or settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthenticationForm(request=request)

    return render(request, "registration/login.html", {
        "form": form,
        "next": next_url,
    })


@csrf_protect
@require_POST
def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
