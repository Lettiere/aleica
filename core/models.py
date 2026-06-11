from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Perfil(TimestampedModel):
    class Codigo(models.TextChoices):
        ROOT = "ROOT", "Root"
        ADMIN_ASSESSORIA = "ADMIN_ASSESSORIA", "Admin Assessoria"
        GESTOR = "GESTOR", "Gestor"
        OPERADOR = "OPERADOR", "Operador"
        CLIENTE_ADMIN = "CLIENTE_ADMIN", "Cliente Admin"
        CLIENTE_USUARIO = "CLIENTE_USUARIO", "Cliente Usuario"

    perfil_id = models.BigAutoField(primary_key=True)
    nome_perfil = models.CharField(max_length=40, choices=Codigo.choices, unique=True)
    descricao = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = '"core"."perfil_tb"'
        constraints = [
            models.UniqueConstraint(fields=["nome_perfil"], name="perfil_nome_perfil_uk"),
        ]

    def __str__(self):
        return self.nome_perfil


class Permissao(TimestampedModel):
    permissao_id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=80, unique=True)
    descricao = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = '"core"."permissao_tb"'
        constraints = [
            models.UniqueConstraint(fields=["codigo"], name="permissao_codigo_uk"),
        ]

    def __str__(self):
        return self.codigo


class Usuario(TimestampedModel):
    usuario_id = models.BigAutoField(primary_key=True)
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="usuario_saas")
    empresa = models.ForeignKey("empresas.Empresa", null=True, blank=True, on_delete=models.PROTECT, db_column="empresa_id_fk", related_name="usuarios")
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, db_column="perfil_id_fk", related_name="usuarios")
    nome = models.CharField(max_length=160)
    email = models.EmailField(max_length=180, unique=True)
    senha_hash = models.CharField(max_length=255)
    ultimo_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = '"core"."usuario_tb"'
        constraints = [
            models.UniqueConstraint(fields=["email"], name="usuario_email_uk"),
        ]

    @property
    def perfil_codigo(self):
        return self.perfil.nome_perfil if self.perfil_id else None

    def __str__(self):
        return self.nome


class UsuarioPermissao(TimestampedModel):
    usuario_permissao_id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column="usuario_id_fk", related_name="permissoes_usuario")
    permissao = models.ForeignKey(Permissao, on_delete=models.CASCADE, db_column="permissao_id_fk", related_name="usuarios_permissao")

    class Meta:
        db_table = '"core"."usuario_permissao_tb"'
        constraints = [
            models.UniqueConstraint(fields=["usuario", "permissao"], name="usuario_permissao_usuario_permissao_uk"),
        ]

    def __str__(self):
        return f"{self.usuario} - {self.permissao}"
