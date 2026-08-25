from django.db import models


class Planta(models.Model):
    nome_cientifico = models.CharField("nome científico", max_length=150)
    nome_popular = models.CharField("nome popular", max_length=150)
    descricao = models.TextField("descrição")
    data_cadastro = models.DateField("data de cadastro", auto_now_add=True)
    status = models.CharField("status", max_length=20, default="ativa")
    data_plantio = models.DateField("data de plantio", null=True, blank=True)
    categoria = models.ForeignKey(
        "categoria.Categoria",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plantas",
        verbose_name="categoria",
    )

    class Meta:
        verbose_name = "planta"
        verbose_name_plural = "plantas"
        ordering = ("nome_popular", "nome_cientifico")

    def __str__(self):
        return f"{self.nome_popular} ({self.nome_cientifico})"
