from django.db import models


class Fotografia(models.Model):
    planta = models.ForeignKey(
        "plantas.Planta",
        on_delete=models.CASCADE,
        related_name="fotografias",
        verbose_name="planta",
    )
    imagem = models.ImageField("imagem", upload_to="plantas/fotografias/")
    data_foto = models.DateField("data da foto")

    class Meta:
        db_table = "plantas_fotografia"
        verbose_name = "fotografia"
        verbose_name_plural = "fotografias"
        ordering = ("-data_foto",)

    def __str__(self):
        return f"{self.planta.nome_popular} — {self.data_foto:%d/%m/%Y}"
