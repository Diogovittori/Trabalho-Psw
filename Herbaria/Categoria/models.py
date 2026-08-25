from django.db import models


class Categoria(models.Model):
    nome = models.CharField("nome", max_length=100, unique=True)
    descricao = models.TextField("descrição", blank=True)

    class Meta:
        db_table = "plantas_categoria"
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        ordering = ("nome",)

    def __str__(self):
        return self.nome
