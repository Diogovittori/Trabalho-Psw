from django.test import TestCase

from Plantas.models import Categoria, Planta

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
        pessoa = Pessoa.objects.create_user(
            username="ana",
            password="senha-segura",
            nome="Ana",
            cpf="123.456.789-00",
            email="ana@example.com",
        )

        pessoa.plantas.add(planta)

        self.assertEqual(list(planta.pessoas.all()), [pessoa])
        self.assertEqual(str(pessoa), "Ana")
