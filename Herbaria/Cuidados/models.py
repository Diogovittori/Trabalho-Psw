from django.db import models


class TipoDeCuidado(models.Model):
    codigo = models.CharField("código", max_length=30, unique=True)
    nome = models.CharField("nome", max_length=100)

    class Meta:
        verbose_name = "tipo de cuidado"
        verbose_name_plural = "tipos de cuidado"
        ordering = ("nome",)

    def __str__(self):
        return self.nome


class Cuidado(models.Model):
    planta = models.ForeignKey(
        "plantas.Planta",
        on_delete=models.CASCADE,
        related_name="cuidados",
        verbose_name="planta",
    )
    tipo = models.ManyToManyField(
        TipoDeCuidado,
        related_name="cuidados",
        verbose_name="tipos de cuidado",
    )
    data = models.DateField("data")
    observacoes = models.TextField("observações", blank=True)

    class Meta:
        db_table = "plantas_cuidados"
        verbose_name = "cuidado"
        verbose_name_plural = "cuidados"
        ordering = ("-data",)

    def __str__(self):
        return (
            f"{self.planta.nome_popular} — {self.get_tipos_display()} "
            f"em {self.data:%d/%m/%Y}"
        )

    def get_tipos_display(self):
        return ", ".join(tipo.nome for tipo in self.tipo.all())

    get_tipos_display.short_description = "cuidado"
