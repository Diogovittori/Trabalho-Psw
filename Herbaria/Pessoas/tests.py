from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from Categoria.models import Categoria
from Plantas.models import Planta

from .models import Pessoa


class PessoaModelTests(TestCase):
    def criar_pessoa(self, cpf):
        usuario = User.objects.create_user(username=f"usuario-{cpf}")
        return Pessoa(
            usuario=usuario,
            nome="Enzo",
            cpf= "529.982.247-25",
            email="Enzovittorio@gmail.com",
        )

    def test_aceita_cpf_matematicamente_valido(self):
        pessoa = self.criar_pessoa("529.982.247-25")

        pessoa.full_clean()

    def test_rejeita_cpf_matematicamente_invalido(self):
        for cpf in ("529.982.247-24", "111.111.111-11", "123"):
            with self.subTest(cpf=cpf):
                pessoa = self.criar_pessoa(cpf)
                with self.assertRaises(ValidationError):
                    pessoa.full_clean()

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
