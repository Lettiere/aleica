from django.db import models


class Empresa(models.Model):
    class Status(models.TextChoices):
        ATIVA = "ativa", "Ativa"
        INATIVA = "inativa", "Inativa"
        PROSPECT = "prospect", "Prospect"

    nome_fantasia = models.CharField(max_length=160)
    razao_social = models.CharField(max_length=190, blank=True)
    cnpj = models.CharField(max_length=24, blank=True)
    segmento = models.CharField(max_length=100)
    telefone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=180, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ATIVA)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_fantasia"]

    def __str__(self):
        return self.nome_fantasia
