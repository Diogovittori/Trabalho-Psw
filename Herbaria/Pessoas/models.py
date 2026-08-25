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
    cpf = models.CharField("CPF", max_length=14, unique=True)
    data_nascimento = models.DateField(
        "data de nascimento", null=True, blank=True
    )
    sexo = models.CharField(
        "sexo", max_length=1, choices=Sexo.choices, blank=True
    )
    telefone = models.CharField("telefone", max_length=20, blank=True)
    numero = models.PositiveIntegerField("número", null=True, blank=True)
    bairro = models.CharField("bairro", max_length=100, blank=True)
    cidade = models.CharField("cidade", max_length=100, blank=True)
    estado = models.CharField("estado", max_length=2, blank=True)
    cep = models.CharField("CEP", max_length=9, blank=True)
    plantas = models.ManyToManyField(
        "plantas.Planta", related_name="pessoas", blank=True
    )

    class Meta:
        verbose_name = "pessoa"
        verbose_name_plural = "pessoas"
        ordering = ("usuario__first_name", "usuario__username")

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username