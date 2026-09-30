from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def eh_funcionario(usuario):
    return usuario.groups.filter(name__in=("Funcionário", "Funcionario", "funcionario", "Funcionários", "funcionarios")).exists()


def pode_gerenciar_pessoas(usuario, acao="view"):
    return (
        getattr(usuario, "is_authenticated", False)
        and usuario.is_active
        and usuario.groups.filter(name__in=("proprietario", "Proprietário")).exists()
        and usuario.has_perm(f"pessoas.{acao}_pessoa")
    )


def proprietario_required(acao):
    def decorator(view):
        @login_required
        @wraps(view)
        def protegida(request, *args, **kwargs):
            if not pode_gerenciar_pessoas(request.user, acao):
                raise PermissionDenied("Esta área é exclusiva do proprietário com a permissão necessária.")
            return view(request, *args, **kwargs)
        return protegida
    return decorator
