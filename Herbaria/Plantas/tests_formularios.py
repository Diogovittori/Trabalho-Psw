import re
from html import escape
from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from Categoria.models import Categoria
from Cuidados.models import TipoDeCuidado
from Plantas.models import Planta


class TextosFormulariosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.editor = User.objects.create_superuser(username="editor-textos", password="Teste!7832")
        cls.categoria = Categoria.objects.create(nome="Ornamentais")
        cls.planta = Planta.objects.create(nome_popular="Rosa", nome_cientifico="Rosa sp.", descricao="Roseira.")

    def verificar_campos(self, resposta):
        self.assertEqual(resposta.status_code, 200)
        html = resposta.content.decode()
        form = resposta.context["form"]
        ids = re.findall(r'\bid="([^"]+)"', html)
        self.assertEqual(len(ids), len(set(ids)), "IDs duplicados na página")
        for campo in form.visible_fields():
            with self.subTest(campo=campo.name):
                if campo.name == "tipo":
                    self.assertContains(resposta, f'<legend class="h6">{campo.label}:</legend>', count=1, html=True)
                else:
                    self.assertEqual(html.count(f'for="{campo.id_for_label}"'), 1)
                    self.assertEqual(html.count(f'name="{campo.html_name}"'), 1)
                if campo.help_text:
                    self.assertEqual(html.count(str(campo.help_text)), 1)
                    self.assertIn(f'id="{campo.auto_id}_helptext"', html)
                if campo.errors:
                    bloco = re.search(rf'id="{campo.auto_id}_errors" role="alert">(.*?)</div></div>', html, re.S)
                    self.assertIsNotNone(bloco)
                    for erro in campo.errors:
                        self.assertEqual(bloco.group(1).count(escape(str(erro))), 1)
        return html

    def test_seis_telas_com_labels_ajuda_e_validacao_sem_duplicacao(self):
        self.client.force_login(self.editor)
        for rota in ("plantas:planta_criar", "plantas:cuidado_criar", "plantas:fotografia_criar", "plantas:categoria_criar", "login", "usuario_cadastrar"):
            with self.subTest(rota=rota):
                self.verificar_campos(self.client.get(reverse(rota)))
                resposta = self.client.post(reverse(rota), {})
                self.verificar_campos(resposta)
                self.assertTrue(resposta.context["form"].errors)
                self.assertContains(resposta, "Confira os campos indicados abaixo e tente novamente.", count=1)

    def test_login_incorreto_exibe_erro_geral_uma_vez(self):
        resposta = self.client.post(reverse("login"), {"username": "editor-textos", "password": "incorreta"})
        self.verificar_campos(resposta)
        self.assertContains(resposta, "Nome de usuário ou senha incorretos. Confira os dados e tente novamente.", count=1)

    def test_cadastro_com_senhas_diferentes_nao_duplica_erro(self):
        resposta = self.client.post(reverse("usuario_cadastrar"), {
            "username": "ana", "nome": "Ana Silva", "email": "ana@example.com", "cpf": "529.982.247-25",
            "password1": "Flor-Jardim!7832", "password2": "Outra-Senha!7832",
        })
        self.verificar_campos(resposta)
        erros = resposta.context["form"].errors["password2"]
        for erro in erros:
            self.assertContains(resposta, erro, count=1)

    def test_erros_categoria_duplicada_e_fotografia_invalida(self):
        self.client.force_login(self.editor)
        resposta = self.client.post(reverse("plantas:categoria_criar"), {"nome": "Ornamentais"})
        self.verificar_campos(resposta)
        self.assertContains(resposta, "Já existe uma categoria com este nome.", count=1)
        resposta = self.client.post(reverse("plantas:fotografia_criar"), {
            "planta": self.planta.pk, "data_foto": "2026-09-29",
            "imagem": SimpleUploadedFile("foto.png", b"invalida", content_type="image/png"),
        })
        self.verificar_campos(resposta)
        self.assertContains(resposta, "Envie um arquivo de imagem válido, como JPG ou PNG.", count=1)

    def test_edicao_preserva_textos_valores_e_botao(self):
        self.client.force_login(self.editor)
        resposta = self.client.get(reverse("plantas:planta_editar", args=[self.planta.pk]))
        self.verificar_campos(resposta)
        self.assertContains(resposta, 'value="Rosa"')
        self.assertContains(resposta, "Salvar alterações", count=1)

    def test_cadastros_exibem_mensagens_de_sucesso(self):
        self.client.force_login(self.editor)
        tipo = TipoDeCuidado.objects.create(codigo="teste_textos", nome="Regar")
        imagem = BytesIO()
        Image.new("RGB", (1, 1)).save(imagem, format="PNG")
        casos = (
            ("categoria", {"nome": "Medicinais"}, "Categoria cadastrada com sucesso."),
            ("planta", {"nome_popular": "Hortelã", "nome_cientifico": "Mentha spicata", "descricao": "Planta aromática."}, "Planta cadastrada com sucesso."),
            ("cuidado", {"planta": self.planta.pk, "tipo": [tipo.pk], "data": "2026-09-29"}, "Cuidado cadastrado com sucesso."),
            ("fotografia", {"planta": self.planta.pk, "data_foto": "2026-09-29", "imagem": SimpleUploadedFile("foto.png", imagem.getvalue(), content_type="image/png")}, "Fotografia cadastrada com sucesso."),
        )
        with TemporaryDirectory() as media, self.settings(MEDIA_ROOT=media):
            for entidade, dados, mensagem in casos:
                with self.subTest(entidade=entidade):
                    resposta = self.client.post(reverse(f"plantas:{entidade}_criar"), dados, follow=True)
                    self.assertRedirects(resposta, reverse(f"plantas:{entidade}_listar"))
                    self.assertContains(resposta, mensagem, count=1)
