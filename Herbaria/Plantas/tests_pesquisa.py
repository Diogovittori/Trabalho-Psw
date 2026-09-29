from datetime import date
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from Categoria.models import Categoria
from Cuidados.models import Cuidados, TipoDeCuidado
from Fotografia.models import Fotografia
from .models import Planta


class PesquisaECardsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user(username="pesquisador")
        cls.categoria = Categoria.objects.create(nome="Flores", descricao="Cultivo ornamental")
        cls.planta = Planta.objects.create(
            nome_popular="Rosa", nome_cientifico="Rosa rubiginosa",
            descricao="Flores perfumadas", categoria=cls.categoria,
            data_plantio=date(2026, 9, 29),
        )
        cls.outra = Planta.objects.create(nome_popular="Cacto", nome_cientifico="Cactaceae", descricao="Suculenta")
        cls.foto = Fotografia.objects.create(planta=cls.planta, imagem="ausente.jpg", data_foto=date(2026, 9, 29))
        cls.cuidado = Cuidados.objects.create(planta=cls.planta, data=date(2026, 9, 29), observacoes="Verificar folhas")
        cls.tipos = [TipoDeCuidado.objects.create(codigo=f"teste_{i}", nome=f"Rega teste {i}") for i in range(2)]
        cls.cuidado.tipo.set(cls.tipos)

    def setUp(self):
        self.client.force_login(self.usuario)

    def test_busca_geral_consulta_registros_e_relacionamentos(self):
        resposta = self.client.get(reverse("plantas:pesquisar"), {"q": "Rosa"})
        self.assertEqual(resposta.context["total"], 3)
        grupos = {g["entidade"]: list(g["objetos"]) for g in resposta.context["grupos"]}
        self.assertEqual(grupos["plantas"], [self.planta])
        self.assertEqual(grupos["fotografias"], [self.foto])
        self.assertEqual(grupos["cuidados"], [self.cuidado])
        self.assertNotContains(resposta, "Cactaceae")

    def test_pesquisa_por_campos_reais_em_cada_app(self):
        for rota, chave, termo, esperado in (
            ("planta", "plantas", "rubiginosa", self.planta),
            ("planta", "plantas", "perfumadas", self.planta),
            ("planta", "plantas", "Flores", self.planta),
            ("fotografia", "fotografias", "rubiginosa", self.foto),
            ("fotografia", "fotografias", "Flores", self.foto),
            ("cuidado", "cuidados", "Verificar folhas", self.cuidado),
            ("cuidado", "cuidados", "Rega teste", self.cuidado),
            ("categoria", "categorias", "ornamental", self.categoria),
        ):
            with self.subTest(rota=rota, termo=termo):
                resposta = self.client.get(reverse(f"plantas:{rota}_listar"), {"q": termo})
                self.assertEqual(list(resposta.context[chave]), [esperado])

    def test_pesquisa_datas_e_tipos_sem_duplicacao(self):
        for rota, chave in (("planta", "plantas"), ("fotografia", "fotografias"), ("cuidado", "cuidados")):
            for termo in ("29/09/2026", "2026-09-29"):
                with self.subTest(rota=rota, termo=termo):
                    resposta = self.client.get(reverse(f"plantas:{rota}_listar"), {"q": termo})
                    self.assertEqual(resposta.context["page_obj"].paginator.count, 1)
        resposta = self.client.get(reverse("plantas:cuidado_listar"), {"q": "Rega teste"})
        self.assertEqual(list(resposta.context["cuidados"]), [self.cuidado])

    def test_pesquisa_aceita_acentos_e_trata_simbolos_como_texto(self):
        planta = Planta.objects.create(nome_popular="Orquídea", nome_cientifico="Phalaenopsis", descricao="Flor")
        for termo in ("orquidea", "ORQUÍDEA", "Orquídea"):
            resposta = self.client.get(reverse("plantas:planta_listar"), {"q": termo})
            self.assertEqual(list(resposta.context["plantas"]), [planta])
        for termo in (".*", "[", "' OR 1=1 --"):
            resposta = self.client.get(reverse("plantas:planta_listar"), {"q": termo})
            self.assertEqual(resposta.context["page_obj"].paginator.count, 0)

    def test_formularios_de_pesquisa_get_apontam_para_rota_correta(self):
        for rota in ("pesquisar", "planta_listar", "fotografia_listar", "cuidado_listar", "categoria_listar"):
            url = reverse(f"plantas:{rota}")
            resposta = self.client.get(url)
            self.assertContains(resposta, f'method="get" action="{url}"')
            self.assertContains(resposta, 'name="q"', count=1)
            self.assertContains(resposta, 'class="input-group"', count=1)

    def test_paginacao_consulta_fora_da_primeira_pagina_e_preserva_termo(self):
        Planta.objects.bulk_create([
            Planta(nome_popular=f"Lote A&B {i:02d}", nome_cientifico="Teste", descricao="Coleção")
            for i in range(25)
        ])
        url = reverse("plantas:planta_listar")
        primeira = self.client.get(url, {"q": "Lote A&B"})
        segunda = self.client.get(url, {"q": "Lote A&B", "page": 2})
        self.assertEqual(primeira.context["page_obj"].paginator.count, 25)
        self.assertEqual(len(primeira.context["plantas"]), 12)
        self.assertEqual(len(segunda.context["plantas"]), 12)
        self.assertContains(primeira, "q=Lote%20A%26B&amp;page=2")
        self.assertFalse(set(primeira.context["plantas"]) & set(segunda.context["plantas"]))
        pesquisa = self.client.get(url, {"q": "Lote A&B 24"})
        self.assertEqual(pesquisa.context["page_obj"].paginator.count, 1)
        self.assertContains(pesquisa, "Lote A&amp;B 24")
        for pagina in ("invalida", "-1", "99999"):
            self.assertEqual(self.client.get(url, {"page": pagina}).status_code, 200)

    def test_busca_vazia_sem_resultado_e_termo_escapado(self):
        resposta = self.client.get(reverse("plantas:pesquisar"), {"q": "   "})
        self.assertEqual(resposta.context["grupos"], [])
        resposta = self.client.get(reverse("plantas:pesquisar"), {"q": '<script>alert("x")</script>'})
        self.assertEqual(resposta.context["total"], 0)
        self.assertNotContains(resposta, '<script>alert("x")</script>')
        self.assertContains(resposta, "Nenhum registro encontrado")

    def test_busca_exige_login_e_cards_respeitam_permissoes(self):
        for rota, pk in (("planta", self.planta.pk), ("fotografia", self.foto.pk)):
            resposta = self.client.get(reverse(f"plantas:{rota}_listar"))
            self.assertContains(resposta, "single-product-area card")
            self.assertNotContains(resposta, "<table")
            self.assertNotContains(resposta, reverse(f"plantas:{rota}_editar", args=[pk]))
            self.assertNotContains(resposta, reverse(f"plantas:{rota}_excluir", args=[pk]))
        self.client.logout()
        self.assertEqual(self.client.get(reverse("plantas:pesquisar"), {"q": "Rosa"}).status_code, 302)

    def test_imagem_ausente_nao_quebra_cards_ou_detalhes(self):
        for rota, args in (("fotografia_listar", []), ("fotografia_detalhar", [self.foto.pk]), ("planta_detalhar", [self.planta.pk])):
            resposta = self.client.get(reverse(f"plantas:{rota}", args=args))
            self.assertContains(resposta, "Imagem indisponível")
            self.assertNotContains(resposta, 'src="/media/ausente.jpg"')


class FluxosAuditadosTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(username="editor-auditoria")
        self.client.force_login(self.usuario)
        self.planta = Planta.objects.create(nome_popular="Rosa", nome_cientifico="Rosa rubiginosa", descricao="Roseira", data_plantio=date(2026, 9, 29))

    def test_datas_de_edicao_em_iso_e_cancelar_sem_javascript(self):
        cuidado = Cuidados.objects.create(planta=self.planta, data=date(2026, 9, 29))
        foto = Fotografia.objects.create(planta=self.planta, data_foto=date(2026, 9, 29), imagem="ausente.jpg")
        for entidade, objeto in (("planta", self.planta), ("cuidado", cuidado), ("fotografia", foto)):
            with self.subTest(entidade=entidade):
                resposta = self.client.get(reverse(f"plantas:{entidade}_editar", args=[objeto.pk]))
                self.assertContains(resposta, 'value="2026-09-29"')
                resposta = self.client.get(reverse(f"plantas:{entidade}_excluir", args=[objeto.pk]))
                self.assertNotContains(resposta, "javascript:")
                self.assertContains(resposta, f'href="{reverse(f"plantas:{entidade}_listar")}"')

    def test_crud_fotografia_com_upload_validado_e_armazenamento_isolado(self):
        with override_settings(STORAGES={
            "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
            "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
        }):
            arquivo = BytesIO()
            Image.new("RGB", (8, 8), "green").save(arquivo, "PNG")
            imagem = SimpleUploadedFile("rosa.png", arquivo.getvalue(), content_type="image/png")
            resposta = self.client.post(reverse("plantas:fotografia_criar"), {
                "planta": self.planta.pk, "data_foto": "2026-09-29", "imagem": imagem,
            }, follow=True)
            self.assertRedirects(resposta, reverse("plantas:fotografia_listar"))
            foto = Fotografia.objects.get()
            self.assertTrue(foto.imagem.storage.exists(foto.imagem.name))
            self.assertContains(resposta, foto.imagem.url)
            resposta = self.client.post(reverse("plantas:fotografia_editar", args=[foto.pk]), {
                "planta": self.planta.pk, "data_foto": "2026-09-30",
            }, follow=True)
            foto.refresh_from_db()
            self.assertEqual(foto.data_foto, date(2026, 9, 30))
            self.assertContains(resposta, "30/09/2026")
            self.assertTrue(foto.imagem.storage.exists(foto.imagem.name))
            self.client.post(reverse("plantas:fotografia_excluir", args=[foto.pk]))
            self.assertFalse(Fotografia.objects.exists())
            self.assertTrue(Planta.objects.filter(pk=self.planta.pk).exists())

    def test_cuidado_salva_varios_tipos_edita_e_exclui(self):
        tipos = list(TipoDeCuidado.objects.all()[:2])
        dados = {"planta": self.planta.pk, "tipo": [t.pk for t in tipos], "data": "2026-09-29", "observacoes": "Rega concluída"}
        resposta = self.client.post(reverse("plantas:cuidado_criar"), dados, follow=True)
        cuidado = Cuidados.objects.get()
        self.assertEqual(set(cuidado.tipo.all()), set(tipos))
        self.assertContains(resposta, "Rega concluída")
        dados.update(tipo=[tipos[0].pk], data="2026-09-30", observacoes="Rega revisada")
        resposta = self.client.post(reverse("plantas:cuidado_editar", args=[cuidado.pk]), dados, follow=True)
        cuidado.refresh_from_db()
        self.assertEqual(list(cuidado.tipo.all()), tipos[:1])
        self.assertEqual(cuidado.data, date(2026, 9, 30))
        self.assertContains(resposta, "Rega revisada")
        self.client.post(reverse("plantas:cuidado_excluir", args=[cuidado.pk]))
        self.assertFalse(Cuidados.objects.exists())

    def test_cuidado_invalido_nao_grava_e_exibe_erro(self):
        resposta = self.client.post(reverse("plantas:cuidado_criar"), {"planta": self.planta.pk, "data": "2026-09-29"})
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("tipo", resposta.context["form"].errors)
        self.assertContains(resposta, 'class="errorlist"')
        self.assertFalse(Cuidados.objects.exists())
