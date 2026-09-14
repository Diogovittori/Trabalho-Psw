from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
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
            content_type = ContentType.objects.get_for_model(modelo)
            modelo_nome = content_type.model

            for acao in ("view", "add", "change", "delete"):
                permissao, _ = Permission.objects.get_or_create(
                    content_type=content_type,
                    codename=f"{acao}_{modelo_nome}",
                    defaults={"name": f"Can {acao} {modelo_nome}"},
                )
                if acao == "view":
                    permissoes_leitores.append(permissao)
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
