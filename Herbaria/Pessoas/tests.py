from django.contrib.auth.models import User
from django.test import TestCase

from Categoria.models import Categoria
from Plantas.models import Planta

from .models import Pessoa


class PessoaModelTests(TestCase):
    def test_pessoa_pode_ter_varias_plantas(self):
        categoria = Categoria.objects.create(nome="Medicinal")
        planta = Planta.objects.create(
            nome_cientifico="Mentha spicata",
            nome_popular="Hortelã",
            descricao="Planta aromática.",
            categoria=categoria,
        )
        usuario = User.objects.create_user(
            username="ana",
            password="senha-segura",
        )
        pessoa = Pessoa.objects.create(
            usuario=usuario,
            nome="Ana",
            cpf=12345678900,
            email="ana@example.com",
        )

        pessoa.plantas.add(planta)

        self.assertEqual(list(planta.pessoas.all()), [pessoa])
        self.assertEqual(str(pessoa), "Ana")
