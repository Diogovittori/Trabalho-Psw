from django.db import models


class Categoria(models.Model):
    nome = models.CharField("nome", max_length=100, unique=True)
    descricao = models.TextField("descrição", blank=True)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        ordering = ("nome",)

    def __str__(self):
        return self.nome


class Planta(models.Model):
    class Status(models.TextChoices):
        ATIVA = "ativa", "Ativa"
        INATIVA = "inativa", "Inativa"

    nome_cientifico = models.CharField("nome científico", max_length=150)
    nome_popular = models.CharField("nome popular", max_length=150)
    descricao = models.TextField("descrição")
    data_cadastro = models.DateField("data de cadastro", auto_now_add=True)
    status = models.CharField(
        "status", max_length=7, choices=Status.choices, default=Status.ATIVA
    )
    data_plantio = models.DateField("data de plantio", null=True, blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="plantas",
        verbose_name="categoria",
    )

    class Meta:
        verbose_name = "planta"
        verbose_name_plural = "plantas"
        ordering = ("nome_popular", "nome_cientifico")

    def __str__(self):
        return f"{self.nome_popular} ({self.nome_cientifico})"


class Cuidados(models.Model):
    planta = models.ForeignKey(
        Planta,
        on_delete=models.CASCADE,
        related_name="cuidados",
        verbose_name="planta",
    )
    tipo = models.BooleanField("cuidado realizado", default=False)
    data = models.DateField("data")
    observacoes = models.TextField("observações", blank=True)

    class Meta:
        verbose_name = "cuidado"
        verbose_name_plural = "cuidados"
        ordering = ("-data",)

    def __str__(self):
        situacao = "realizado" if self.tipo else "pendente"
        return f"{self.planta.nome_popular} — {situacao} em {self.data:%d/%m/%Y}"


class Fotografia(models.Model):
    planta = models.ForeignKey(
        Planta,
        on_delete=models.CASCADE,
        related_name="fotografias",
        verbose_name="planta",
    )
    imagem = models.ImageField("imagem", upload_to="plantas/fotografias/")
    data_foto = models.DateField("data da foto")

    class Meta:
        verbose_name = "fotografia"
        verbose_name_plural = "fotografias"
        ordering = ("-data_foto",)

    def __str__(self):
        return f"{self.planta.nome_popular} — {self.data_foto:%d/%m/%Y}"