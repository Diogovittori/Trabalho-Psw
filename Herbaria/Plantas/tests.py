from datetime import date

from django.db.models.deletion import ProtectedError
from django.test import TestCase

from .models import Categoria, Cuidados, Fotografia, Planta


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

    def test_relacionamentos_da_planta(self):
        cuidado = Cuidados.objects.create(
            planta=self.planta,
            tipo=True,
            data=date(2026, 8, 18),
            observacoes="Rega concluída.",
        )
        fotografia = Fotografia.objects.create(
            planta=self.planta,
            imagem="plantas/fotografias/costela.jpg",
            data_foto=date(2026, 8, 18),
        )

        self.assertEqual(list(self.categoria.plantas.all()), [self.planta])
        self.assertEqual(list(self.planta.cuidados.all()), [cuidado])
        self.assertEqual(list(self.planta.fotografias.all()), [fotografia])

    def test_categoria_em_uso_nao_pode_ser_excluida(self):
        with self.assertRaises(ProtectedError):
            self.categoria.delete()
