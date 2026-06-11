from django.db import models

from core.managers import EmpresaRootScopedManager


class Empresa(models.Model):
    class Status(models.TextChoices):
        ATIVA = "ativa", "Ativa"
        INATIVA = "inativa", "Inativa"
        PROSPECT = "prospect", "Prospect"

    empresa_id = models.BigAutoField(primary_key=True)
    razao_social = models.CharField(max_length=190, blank=True)
    nome_fantasia = models.CharField(max_length=160)
    cnpj = models.CharField(max_length=24, blank=True)
    email = models.EmailField(max_length=180, blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ATIVA)
    segmento = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = EmpresaRootScopedManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["nome_fantasia"]
        db_table = '"core"."empresa_tb"'

    def __str__(self):
        return self.nome_fantasia
