from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from core.models import Perfil, Permissao, Usuario


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["nome_perfil", "descricao", "ativo"]
        widgets = {
            "nome_perfil": forms.Select(attrs={"class": "form-select"}),
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PermissaoForm(forms.ModelForm):
    class Meta:
        model = Permissao
        fields = ["codigo", "descricao", "ativo"]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "modulo:acao"}),
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class UsuarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    class Meta:
        model = Usuario
        fields = ["nome", "email", "empresa", "perfil", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "empresa": forms.Select(attrs={"class": "form-select"}),
            "perfil": forms.Select(attrs={"class": "form-select"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.instance, "auth_user", None)
        if user:
            self.fields["username"].initial = user.username
            self.fields["is_staff"].initial = user.is_staff
        else:
            self.fields["password"].required = True
        self.fields["password"].help_text = "Obrigatoria ao criar. Em branco mantem a senha atual ao editar."

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password)
        return password

    def clean_username(self):
        username = self.cleaned_data["username"]
        qs = User.objects.filter(username=username)
        auth_user = getattr(self.instance, "auth_user", None)
        if auth_user:
            qs = qs.exclude(pk=auth_user.pk)
        if qs.exists():
            raise forms.ValidationError("Ja existe um auth_user com este usuario.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = Usuario.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ja existe um usuario Aleica com este email.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        usuario = super().save(commit=False)
        username = self.cleaned_data["username"]
        password = self.cleaned_data.get("password")
        auth_user = usuario.auth_user
        if auth_user is None:
            auth_user = User(username=username)
        auth_user.username = username
        auth_user.email = usuario.email
        partes = usuario.nome.split(" ", 1)
        auth_user.first_name = partes[0]
        auth_user.last_name = partes[1] if len(partes) > 1 else ""
        auth_user.is_staff = self.cleaned_data.get("is_staff", False)
        auth_user.is_active = usuario.ativo
        if password:
            auth_user.set_password(password)
        auth_user.save()
        usuario.auth_user = auth_user
        usuario.senha_hash = auth_user.password
        if commit:
            usuario.save()
        return usuario
