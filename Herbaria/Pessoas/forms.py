from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Pessoa, validar_cpf


class PessoaCadastroForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha", widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirme a senha", widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    class Meta:
        model = Pessoa
        fields = ("username", "email", "nome", "cpf")

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        validar_cpf(cpf)
        if Pessoa.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "As senhas não conferem.")
        elif password1:
            usuario = Pessoa(
                username=cleaned_data.get("username", ""),
                email=cleaned_data.get("email", ""),
                nome=cleaned_data.get("nome", ""),
            )
            try:
                password_validation.validate_password(password1, usuario)
            except ValidationError as erro:
                self.add_error("password1", erro)

        return cleaned_data

    def save(self, commit=True):
        pessoa = super().save(commit=False)
        pessoa.set_password(self.cleaned_data["password1"])
        if commit:
            pessoa.save()
        return pessoa
