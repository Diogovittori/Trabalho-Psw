from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction

from Categoria.models import Categoria
from Cuidados.models import Cuidados
from Fotografia.models import Fotografia
from Plantas.models import Planta


class Command(BaseCommand):
    help = "Cria os grupos de leitores e editores do Herbaria."

    @transaction.atomic
    def handle(self, *args, **options):
        modelos = (Categoria, Planta, Cuidados, Fotografia)
        permissoes_leitores = []
        permissoes_editores = []

        for modelo in modelos:
            app_label = modelo._meta.app_label
            model_name = modelo._meta.model_name

            permissao_view = Permission.objects.get(
                content_type__app_label=app_label,
                content_type__model=model_name,
                codename=f"view_{model_name}",
            )
            permissoes_leitores.append(permissao_view)

            for acao in ("view", "add", "change", "delete"):
                permissao = Permission.objects.get(
                    content_type__app_label=app_label,
                    content_type__model=model_name,
                    codename=f"{acao}_{model_name}",
                )
                permissoes_editores.append(permissao)

        grupo_leitores, _ = Group.objects.get_or_create(
            name="Herbaria - Leitores"
        )
        grupo_editores, _ = Group.objects.get_or_create(
            name="Herbaria - Editores"
        )

        grupo_leitores.permissions.set(permissoes_leitores)
        grupo_editores.permissions.set(permissoes_editores)

        self.stdout.write(
            self.style.SUCCESS("Grupos de permissões criados com sucesso.")
        )
