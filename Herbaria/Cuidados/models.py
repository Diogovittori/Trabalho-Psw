from django.db import models


class Cuidados(models.Model):
    planta = models.ForeignKey(
        "plantas.Planta",
        on_delete=models.CASCADE,
        related_name="cuidados",
        verbose_name="planta",
    )
    tipo = models.BooleanField("tipo")
    data = models.DateField("data")
    observacoes = models.TextField("observações", blank=True)

    class Meta:
        db_table = "plantas_cuidados"
        verbose_name = "cuidado"
        verbose_name_plural = "cuidados"
        ordering = ("-data",)

    def __str__(self):
        return f"{self.planta.nome_popular} — {self.data:%d/%m/%Y}"
