from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from Categoria.models import Categoria
from Plantas.models import Planta

from .models import Pessoa


class PessoaModelTests(TestCase):
    def criar_pessoa(self, cpf):
        return Pessoa(
            username=f"usuario-{cpf}",
            password="senha-segura",
            nome="Enzo",
            cpf=cpf,
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
        pessoa = Pessoa.objects.create_user(
            username="ana",
            password="senha-segura",
            nome="Ana",
            cpf=12345678900,
            email="ana@example.com",
        )

        pessoa.plantas.add(planta)

        self.assertEqual(list(planta.pessoas.all()), [pessoa])
        self.assertEqual(str(pessoa), "Ana")


class CadastroPessoaTests(TestCase):
    def test_cadastro_salva_senha_e_login_funciona_sem_permissao_de_edicao(self):
        resposta = self.client.post(reverse("usuario_cadastrar"), {
            "username": "novo-observador", "nome": "Observador", "cpf": "529.982.247-25",
            "data_nascimento": "2000-01-15", "telefone": "11999999999",
            "email": "observador@example.com", "password1": "Flor-Jardim!7832", "password2": "Flor-Jardim!7832",
        })
        self.assertRedirects(resposta, reverse("login"))
        pessoa = Pessoa.objects.get(username="novo-observador")
        self.assertEqual(pessoa.cpf, "52998224725")
        self.assertTrue(pessoa.check_password("Flor-Jardim!7832"))
        self.assertTrue(pessoa.groups.filter(name="Observadores").exists())
        resposta = self.client.post(reverse("login"), {"username": pessoa.username, "password": "Flor-Jardim!7832"})
        self.assertRedirects(resposta, reverse("plantas:planta_listar"))
        self.assertEqual(self.client.get(reverse("plantas:pesquisar"), {"q": "Rosa"}).status_code, 200)
        for entidade in ("planta", "fotografia", "cuidado", "categoria"):
            self.assertEqual(self.client.post(reverse(f"plantas:{entidade}_criar"), {}).status_code, 403)

    def test_cpf_invalido_nao_cria_usuario(self):
        resposta = self.client.post(reverse("usuario_cadastrar"), {
            "username": "invalido", "nome": "Teste", "cpf": "11111111111", "email": "teste@example.com",
            "password1": "Flor-Jardim!7832", "password2": "Flor-Jardim!7832",
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("cpf", resposta.context["form"].errors)
        self.assertFalse(Pessoa.objects.filter(username="invalido").exists())
