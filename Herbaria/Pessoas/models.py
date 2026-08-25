from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validar_cpf(valor):
    cpf = "".join(caractere for caractere in str(valor) if caractere.isdigit())

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("Informe um CPF válido.", code="cpf_invalido")

    for posicao in (9, 10):
        soma = sum(
            int(cpf[indice]) * (posicao + 1 - indice)
            for indice in range(posicao)
        )
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[posicao]):
            raise ValidationError(
                "Informe um CPF válido.", code="cpf_invalido"
            )


class Pessoa(User):
    class Sexo(models.TextChoices):
        FEMININO = "F", "Feminino"
        MASCULINO = "M", "Masculino"
        OUTRO = "O", "Outro"
        NAO_INFORMADO = "N", "Prefiro não informar"

    nome = models.CharField("nome", max_length=150, default="")
    cpf = models.CharField(
        "CPF", max_length=14, unique=True, validators=[validar_cpf]
    )
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
