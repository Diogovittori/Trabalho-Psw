from django.contrib import messages
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import PessoaCadastroForm


def usuario_cadastrar(request):
    if request.method == "POST":
        form = PessoaCadastroForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                pessoa = form.save()
                grupo, _ = Group.objects.get_or_create(name="Observadores")
                pessoa.groups.add(grupo)
            messages.success(
                request,
                "Cadastro concluído. Faça login para continuar.",
            )
            return redirect("login")
    else:
        form = PessoaCadastroForm()

    return render(
        request,
        "Pessoas/usuario_formulario.html",
        {"form": form, "titulo": "Cadastrar usuário"},
    )
