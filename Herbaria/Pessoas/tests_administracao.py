from django.contrib.auth.models import Group, Permission, User
from django.test import Client, TestCase
from django.urls import reverse

from Plantas.models import Planta
from .models import Pessoa


class AdministracaoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dono = User.objects.create_user(username="proprietario-teste")
        cls.dono.groups.add(Group.objects.get(name="proprietario"))
        cls.usuario = User.objects.create_user(username="funcionario-teste", password="Senha!7832")
        cls.grupo = Group.objects.create(name="Funcionário")
        cls.usuario.groups.add(cls.grupo)
        cls.planta = Planta.objects.create(nome_popular="Rosa", nome_cientifico="Rosa sp.", descricao="Roseira")

    def setUp(self):
        self.client.force_login(self.dono)
        self.urls = [reverse("pessoas:pessoa_listar")] + [
            reverse(f"pessoas:pessoa_{acao}", args=[self.usuario.pk]) for acao in ("detalhar", "editar", "excluir")
        ]

    def test_proprietario_acessa_todas_as_paginas(self):
        for url in self.urls:
            self.assertEqual(self.client.get(url).status_code, 200)
        self.assertContains(self.client.get(self.urls[0]), self.usuario.username)

    def test_anonimo_e_funcionario_nao_acessam(self):
        self.client.logout()
        for url in self.urls:
            self.assertEqual(self.client.get(url).status_code, 302)
        self.usuario.user_permissions.set(Permission.objects.filter(content_type__app_label="pessoas"))
        self.client.force_login(self.usuario)
        for url in self.urls:
            self.assertEqual(self.client.get(url).status_code, 403)
            self.assertEqual(self.client.post(url).status_code, 403)

    def test_grupo_legado_funciona_e_permissao_continua_obrigatoria(self):
        grupo = Group.objects.create(name="Proprietário")
        self.dono.groups.set([grupo])
        self.assertEqual(self.client.get(self.urls[0]).status_code, 403)
        grupo.permissions.add(Permission.objects.get(content_type__app_label="pessoas", codename="view_pessoa"))
        self.assertEqual(self.client.get(self.urls[0]).status_code, 200)
        self.assertEqual(self.client.post(self.urls[2]).status_code, 403)

    def test_edicao_completa_perfil_sem_mudar_senha_ou_grupos(self):
        dados = {"username": self.usuario.username, "nome": "Funcionário", "cpf": "529.982.247-25",
                 "email": "teste@example.com", "data_nascimento": "2000-01-15", "telefone": "11999999999",
                 "plantas": [self.planta.pk], "is_superuser": "on", "groups": [self.dono.groups.first().pk]}
        self.assertRedirects(self.client.post(self.urls[2], dados), self.urls[0])
        pessoa = Pessoa.objects.get(pk=self.usuario.pk)
        self.assertTrue(pessoa.check_password("Senha!7832"))
        self.assertFalse(pessoa.is_superuser)
        self.assertEqual(list(pessoa.groups.all()), [self.grupo])
        self.assertEqual(list(pessoa.plantas.all()), [self.planta])
        pessoa.groups.clear()
        self.assertNotContains(self.client.get(self.urls[2]), 'name="plantas"')
        self.assertNotContains(self.client.get(self.urls[1]), "Plantas vinculadas")

    def test_exclusao_exige_post_csrf_e_impede_autoexclusao(self):
        self.client.get(self.urls[3])
        self.assertTrue(User.objects.filter(pk=self.usuario.pk).exists())
        protegido = Client(enforce_csrf_checks=True)
        protegido.force_login(self.dono)
        self.assertEqual(protegido.post(self.urls[3]).status_code, 403)
        self.client.post(reverse("pessoas:pessoa_excluir", args=[self.dono.pk]))
        self.assertTrue(User.objects.filter(pk=self.dono.pk).exists())
        self.assertRedirects(self.client.post(self.urls[3]), self.urls[0])
        self.assertFalse(User.objects.filter(pk=self.usuario.pk).exists())
        self.assertTrue(Planta.objects.filter(pk=self.planta.pk).exists())
