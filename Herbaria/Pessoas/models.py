from django.contrib.auth.models import User
from django.db import models


class Pessoa(models.Model):
    class Sexo(models.TextChoices):
        FEMININO = "F", "Feminino"
        MASCULINO = "M", "Masculino"
        OUTRO = "O", "Outro"
        NAO_INFORMADO = "N", "Prefiro não informar"

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="pessoa",
        verbose_name="usuário",
    )
    nome = models.CharField("nome", max_length=150, default="")
    cpf = models.PositiveBigIntegerField("CPF", unique=True)
    data_nascimento = models.DateField(
        "data de nascimento", null=True, blank=True
    )
    sexo = models.CharField(
        "sexo", max_length=1, choices=Sexo.choices, blank=True
    )
    email = models.EmailField("e-mail", default="")
    telefone = models.CharField("telefone", max_length=20, blank=True)
    numero = models.PositiveIntegerField("número", null=True, blank=True)
    bairro = models.CharField("bairro", max_length=100, blank=True)
    cidade = models.CharField("cidade", max_length=100, blank=True)
    estado = models.CharField("estado", max_length=2, blank=True)
    cep = models.PositiveIntegerField("CEP", null=True, blank=True)
    plantas = models.ManyToManyField(
        "plantas.Planta", related_name="pessoas", blank=True
    )

    class Meta:
        verbose_name = "pessoa"
        verbose_name_plural = "pessoas"
        ordering = ("nome",)

    def __str__(self):
        return self.nome
