from datetime import date
from io import StringIO

from django.contrib.auth.models import Group, Permission, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from Categoria.models import Categoria
from Cuidados.models import Cuidados, TipoDeCuidado
from Fotografia.models import Fotografia
from Pessoas.models import Pessoa
from Plantas.models import Planta


MODELOS_PROTEGIDOS = (Categoria, Planta, Cuidados, Fotografia)


def obter_permissoes(modelos, acoes):
    permissoes = []
    for modelo in modelos:
        app_label = modelo._meta.app_label
        model_name = modelo._meta.model_name
        for acao in acoes:
            permissoes.append(
                Permission.objects.get(
                    content_type__app_label=app_label,
                    content_type__model=model_name,
                    codename=f"{acao}_{model_name}",
                )
            )
    return permissoes


def criar_usuario_em_grupo(username, nome_grupo, acoes):
    grupo, _ = Group.objects.get_or_create(name=nome_grupo)
    grupo.permissions.set(obter_permissoes(MODELOS_PROTEGIDOS, acoes))
    usuario = User.objects.create_user(
        username=username,
        password="senha-segura",
    )
    usuario.groups.add(grupo)
    return usuario


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
        self.editor = criar_usuario_em_grupo(
            "editor-crud",
            "Herbaria - Editores",
            ("view", "add", "change", "delete"),
        )
        self.client.force_login(self.editor)

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


class AutenticacaoTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username="usuario-login",
            password="senha-segura",
        )
        self.categoria = Categoria.objects.create(nome="Autenticação")
        self.planta = Planta.objects.create(
            nome_cientifico="Lavandula angustifolia",
            nome_popular="Lavanda",
            descricao="Planta aromática.",
            categoria=self.categoria,
        )

    def test_listagens_protegidas_redirecionam_anonimo_para_login(self):
        for nome in (
            "plantas:categoria_listar",
            "plantas:planta_listar",
            "plantas:cuidado_listar",
            "plantas:fotografia_listar",
        ):
            with self.subTest(url=nome):
                url = reverse(nome)
                resposta = self.client.get(url)
                self.assertRedirects(
                    resposta,
                    f"{reverse('login')}?next={url}",
                )

    def test_detalhe_protegido_redireciona_anonimo_com_next(self):
        url = reverse("plantas:planta_detalhar", args=[self.planta.pk])

        resposta = self.client.get(url)

        self.assertRedirects(resposta, f"{reverse('login')}?next={url}")

    def test_usuario_valido_consegue_login_e_recebe_redirecionamento_padrao(self):
        resposta = self.client.post(
            reverse("login"),
            {"username": self.usuario.username, "password": "senha-segura"},
        )

        self.assertRedirects(resposta, reverse("plantas:planta_listar"))
        self.assertTrue(resposta.wsgi_request.user.is_authenticated)

    def test_login_preserva_next_valido(self):
        destino = reverse("plantas:planta_detalhar", args=[self.planta.pk])

        resposta = self.client.post(
            reverse("login"),
            {
                "username": self.usuario.username,
                "password": "senha-segura",
                "next": destino,
            },
        )

        self.assertRedirects(resposta, destino)

    def test_logout_por_post_volta_a_exigir_autenticacao(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse("logout"))

        self.assertRedirects(resposta, reverse("login"))
        url_protegida = reverse("plantas:planta_listar")
        resposta = self.client.get(url_protegida)
        self.assertRedirects(
            resposta,
            f"{reverse('login')}?next={url_protegida}",
        )


class PermissoesDeViewsETemplatesTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Permissões")
        self.planta = Planta.objects.create(
            nome_cientifico="Salvia officinalis",
            nome_popular="Sálvia",
            descricao="Planta medicinal.",
            categoria=self.categoria,
        )
        self.tipo = TipoDeCuidado.objects.create(
            codigo="teste_permissoes",
            nome="Teste de permissões",
        )
        self.cuidado = Cuidados.objects.create(
            planta=self.planta,
            data=date(2026, 9, 13),
        )
        self.cuidado.tipo.add(self.tipo)
        self.fotografia = Fotografia.objects.create(
            planta=self.planta,
            imagem="plantas/fotografias/permissoes.jpg",
            data_foto=date(2026, 9, 13),
        )
        self.leitor = criar_usuario_em_grupo(
            "leitor",
            "Herbaria - Leitores",
            ("view",),
        )
        self.editor = criar_usuario_em_grupo(
            "editor",
            "Herbaria - Editores",
            ("view", "add", "change", "delete"),
        )
        self.entidades = (
            ("categoria", self.categoria),
            ("planta", self.planta),
            ("cuidado", self.cuidado),
            ("fotografia", self.fotografia),
        )

    def test_leitor_acessa_listagens_e_detalhes(self):
        self.client.force_login(self.leitor)
        for nome, objeto in self.entidades:
            with self.subTest(entidade=nome, pagina="listagem"):
                self.assertEqual(
                    self.client.get(reverse(f"plantas:{nome}_listar")).status_code,
                    200,
                )
            with self.subTest(entidade=nome, pagina="detalhe"):
                self.assertEqual(
                    self.client.get(
                        reverse(f"plantas:{nome}_detalhar", args=[objeto.pk])
                    ).status_code,
                    200,
                )

    def test_leitor_recebe_403_em_criacao_edicao_e_exclusao(self):
        self.client.force_login(self.leitor)
        for nome, objeto in self.entidades:
            for acao, args in (
                ("criar", []),
                ("editar", [objeto.pk]),
                ("excluir", [objeto.pk]),
            ):
                with self.subTest(entidade=nome, acao=acao):
                    resposta = self.client.get(
                        reverse(f"plantas:{nome}_{acao}", args=args)
                    )
                    self.assertEqual(resposta.status_code, 403)

    def test_editor_acessa_criacao_edicao_e_exclusao(self):
        self.client.force_login(self.editor)
        for nome, objeto in self.entidades:
            for acao, args in (
                ("criar", []),
                ("editar", [objeto.pk]),
                ("excluir", [objeto.pk]),
            ):
                with self.subTest(entidade=nome, acao=acao):
                    resposta = self.client.get(
                        reverse(f"plantas:{nome}_{acao}", args=args)
                    )
                    self.assertEqual(resposta.status_code, 200)

    def test_templates_escondem_acoes_do_leitor(self):
        self.client.force_login(self.leitor)
        for nome, objeto in self.entidades:
            with self.subTest(entidade=nome, pagina="listagem"):
                resposta = self.client.get(reverse(f"plantas:{nome}_listar"))
                self.assertNotContains(resposta, reverse(f"plantas:{nome}_criar"))
                self.assertNotContains(
                    resposta,
                    reverse(f"plantas:{nome}_editar", args=[objeto.pk]),
                )
                self.assertNotContains(
                    resposta,
                    reverse(f"plantas:{nome}_excluir", args=[objeto.pk]),
                )
            with self.subTest(entidade=nome, pagina="detalhe"):
                resposta = self.client.get(
                    reverse(f"plantas:{nome}_detalhar", args=[objeto.pk])
                )
                self.assertNotContains(
                    resposta,
                    reverse(f"plantas:{nome}_editar", args=[objeto.pk]),
                )
                self.assertNotContains(
                    resposta,
                    reverse(f"plantas:{nome}_excluir", args=[objeto.pk]),
                )

    def test_templates_exibem_acoes_do_editor(self):
        self.client.force_login(self.editor)
        for nome, objeto in self.entidades:
            with self.subTest(entidade=nome, pagina="listagem"):
                resposta = self.client.get(reverse(f"plantas:{nome}_listar"))
                self.assertContains(resposta, reverse(f"plantas:{nome}_criar"))
            with self.subTest(entidade=nome, pagina="detalhe"):
                resposta = self.client.get(
                    reverse(f"plantas:{nome}_detalhar", args=[objeto.pk])
                )
                self.assertContains(
                    resposta,
                    reverse(f"plantas:{nome}_editar", args=[objeto.pk]),
                )
                self.assertContains(
                    resposta,
                    reverse(f"plantas:{nome}_excluir", args=[objeto.pk]),
                )


class CriarGruposCommandTests(TestCase):
    def executar_comando(self):
        saida = StringIO()
        call_command("criar_grupos", stdout=saida)
        return saida.getvalue()

    def test_comando_cria_grupos_com_permissoes_corretas_e_e_idempotente(self):
        self.executar_comando()

        leitores = Group.objects.get(name="Herbaria - Leitores")
        editores = Group.objects.get(name="Herbaria - Editores")
        esperadas_leitores = obter_permissoes(MODELOS_PROTEGIDOS, ("view",))
        esperadas_editores = obter_permissoes(
            MODELOS_PROTEGIDOS,
            ("view", "add", "change", "delete"),
        )

        self.assertSetEqual(
            set(leitores.permissions.all()),
            set(esperadas_leitores),
        )
        self.assertSetEqual(
            set(editores.permissions.all()),
            set(esperadas_editores),
        )
        self.assertSetEqual(
            set(
                editores.permissions.filter(
                    content_type__app_label="cuidados",
                    content_type__model="cuidados",
                ).values_list("codename", flat=True)
            ),
            {
                "view_cuidados",
                "add_cuidados",
                "change_cuidados",
                "delete_cuidados",
            },
        )

        self.executar_comando()

        self.assertEqual(
            Group.objects.filter(name="Herbaria - Leitores").count(),
            1,
        )
        self.assertEqual(
            Group.objects.filter(name="Herbaria - Editores").count(),
            1,
        )
