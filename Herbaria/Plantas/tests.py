from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Categoria.models import Categoria
from Cuidados.models import Cuidados, TipoDeCuidado
from Fotografia.models import Fotografia
from Pessoas.models import Pessoa
from Plantas.models import Planta


class PlantaModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome="Ornamental", descricao="Plantas usadas na decoração."
        )
        self.planta = Planta.objects.create(
            nome_cientifico="Monstera deliciosa",
            nome_popular="Costela-de-adão",
            descricao="Planta tropical.",
            data_plantio=date(2026, 1, 10),
            categoria=self.categoria,
        )
        self.tipo, _ = TipoDeCuidado.objects.get_or_create(
            codigo="regar_moderadamente", nome="Regar moderadamente"
        )

    def test_relacionamentos_da_planta(self):
        cuidado = Cuidados.objects.create(
            planta=self.planta,
            data=date(2026, 8, 18),
            observacoes="Rega concluída.",
        )
        cuidado.tipo.add(self.tipo)
        fotografia = Fotografia.objects.create(
            planta=self.planta,
            imagem="plantas/fotografias/costela.jpg",
            data_foto=date(2026, 8, 18),
        )

        self.assertEqual(list(self.categoria.plantas.all()), [self.planta])
        self.assertEqual(list(self.planta.cuidados.all()), [cuidado])
        self.assertEqual(list(self.planta.fotografias.all()), [fotografia])

    def test_categoria_em_uso_pode_ser_excluida_sem_apagar_planta(self):
        self.categoria.delete()

        self.planta.refresh_from_db()
        self.assertIsNone(self.planta.categoria)

    def test_excluir_planta_preserva_integridade_dos_relacionamentos(self):
        cuidado = Cuidados.objects.create(
            planta=self.planta,
            data=date(2026, 8, 25),
        )
        cuidado.tipo.add(self.tipo)
        fotografia = Fotografia.objects.create(
            planta=self.planta,
            imagem="plantas/fotografias/planta.jpg",
            data_foto=date(2026, 8, 25),
        )
        usuario = User.objects.create_user(username="jardineiro")
        pessoa = Pessoa.objects.create(
            usuario=usuario,
            nome="Jardineiro",
            cpf="529.982.247-25",
            email="jardineiro@example.com",
        )
        pessoa.plantas.add(self.planta)

        self.planta.delete()

        self.assertFalse(Cuidados.objects.filter(pk=cuidado.pk).exists())
        self.assertFalse(Fotografia.objects.filter(pk=fotografia.pk).exists())
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())
        self.assertTrue(TipoDeCuidado.objects.filter(pk=self.tipo.pk).exists())
        self.assertTrue(Pessoa.objects.filter(pk=pessoa.pk).exists())
        self.assertFalse(pessoa.plantas.exists())


class PlantaViewTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome="Medicinal", descricao="Plantas para uso medicinal."
        )
        self.tipo, _ = TipoDeCuidado.objects.get_or_create(
            codigo="regar_pouco", nome="Regar pouco"
        )

    def test_paginas_de_listagem_respondem(self):
        nomes = (
            "plantas:categoria_listar",
            "plantas:planta_listar",
            "plantas:cuidado_listar",
            "plantas:fotografia_listar",
        )
        for nome in nomes:
            with self.subTest(url=nome):
                self.assertEqual(self.client.get(reverse(nome)).status_code, 200)

    def test_formulario_de_cuidado_exibe_tipos_cadastrados(self):
        resposta = self.client.get(reverse("plantas:cuidado_criar"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(
            resposta,
            'type="checkbox"',
            count=TipoDeCuidado.objects.count(),
        )
        self.assertContains(resposta, "Regar muito")
        self.assertContains(resposta, "Adubar")
        self.assertContains(resposta, "Colocar em local iluminado")

    def test_cria_categoria(self):
        resposta = self.client.post(
            reverse("plantas:categoria_criar"),
            {"nome": "Ornamental", "descricao": "Uso decorativo."},
        )
        self.assertRedirects(resposta, reverse("plantas:categoria_listar"))
        self.assertTrue(Categoria.objects.filter(nome="Ornamental").exists())

    def test_cria_planta(self):
        resposta = self.client.post(
            reverse("plantas:planta_criar"),
            {
                "nome_cientifico": "Mentha spicata",
                "nome_popular": "Hortelã",
                "descricao": "Planta aromática.",
                "data_plantio": "2026-08-20",
                "categoria": self.categoria.pk,
            },
        )
        self.assertRedirects(resposta, reverse("plantas:planta_listar"))
        self.assertTrue(Planta.objects.filter(nome_popular="Hortelã").exists())

    def test_cria_cuidado(self):
        planta = Planta.objects.create(
            nome_cientifico="Aloe vera",
            nome_popular="Babosa",
            descricao="Suculenta.",
            categoria=self.categoria,
        )
        resposta = self.client.post(
            reverse("plantas:cuidado_criar"),
            {
                "planta": planta.pk,
                "tipo": [self.tipo.pk],
                "data": "2026-08-23",
                "observacoes": "Rega realizada.",
            },
        )
        self.assertRedirects(resposta, reverse("plantas:cuidado_listar"))
        cuidado = Cuidados.objects.get(planta=planta)
        self.assertEqual(list(cuidado.tipo.all()), [self.tipo])

    def test_crud_completo_das_entidades(self):
        planta = Planta.objects.create(
            nome_cientifico="Ocimum basilicum",
            nome_popular="Manjericão",
            descricao="Planta aromática.",
            categoria=self.categoria,
        )
        cuidado = Cuidados.objects.create(
            planta=planta,
            data=date(2026, 8, 23),
        )
        cuidado.tipo.add(self.tipo)
        fotografia = Fotografia.objects.create(
            planta=planta,
            imagem="plantas/fotografias/manjericao.jpg",
            data_foto=date(2026, 8, 23),
        )

        objetos = (
            ("categoria", self.categoria),
            ("planta", planta),
            ("cuidado", cuidado),
            ("fotografia", fotografia),
        )
        for nome, objeto in objetos:
            with self.subTest(entidade=nome):
                self.assertEqual(
                    self.client.get(
                        reverse(f"plantas:{nome}_detalhar", args=[objeto.pk])
                    ).status_code,
                    200,
                )
                self.assertEqual(
                    self.client.get(
                        reverse(f"plantas:{nome}_editar", args=[objeto.pk])
                    ).status_code,
                    200,
                )
                self.assertEqual(
                    self.client.get(
                        reverse(f"plantas:{nome}_excluir", args=[objeto.pk])
                    ).status_code,
                    200,
                )

        resposta = self.client.post(
            reverse("plantas:planta_editar", args=[planta.pk]),
            {
                "nome_cientifico": planta.nome_cientifico,
                "nome_popular": "Manjericão-roxo",
                "descricao": planta.descricao,
                "data_plantio": "",
                "categoria": self.categoria.pk,
            },
        )
        self.assertRedirects(resposta, reverse("plantas:planta_listar"))
        planta.refresh_from_db()
        self.assertEqual(planta.nome_popular, "Manjericão-roxo")

        resposta = self.client.post(
            reverse("plantas:categoria_excluir", args=[self.categoria.pk])
        )
        self.assertRedirects(resposta, reverse("plantas:categoria_listar"))
        self.assertFalse(Categoria.objects.filter(pk=self.categoria.pk).exists())
        planta.refresh_from_db()
        self.assertIsNone(planta.categoria)

        for nome, objeto, modelo in (
            ("fotografia", fotografia, Fotografia),
            ("cuidado", cuidado, Cuidados),
            ("planta", planta, Planta),
        ):
            with self.subTest(excluir=nome):
                resposta = self.client.post(
                    reverse(f"plantas:{nome}_excluir", args=[objeto.pk])
                )
                self.assertEqual(resposta.status_code, 302)
                self.assertFalse(modelo.objects.filter(pk=objeto.pk).exists())
