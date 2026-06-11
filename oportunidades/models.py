from django.db import models

from core.managers import EmpresaScopedManager
from clientes.models import Cliente
from empresas.models import Empresa


class Oportunidade(models.Model):
    class Prioridade(models.TextChoices):
        BAIXO = "baixo", "Baixo"
        MEDIO = "medio", "Medio"
        ALTO = "alto", "Alto"
        CRITICO = "critico", "Critico"

    class Status(models.TextChoices):
        ABERTA = "aberta", "Aberta"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDA = "concluida", "Concluida"
        PERDIDA = "perdida", "Perdida"

    oportunidade_id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column="cliente_id_fk", related_name="oportunidades")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column="empresa_id_fk", related_name="oportunidades")
    tipo = models.CharField(max_length=90)
    prioridade = models.CharField(max_length=20, choices=Prioridade.choices, default=Prioridade.BAIXO)
    score = models.PositiveIntegerField(default=0)
    probabilidade_perda = models.PositiveIntegerField(default=0)
    valor_potencial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    motivo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    acao_sugerida = models.CharField(max_length=255)
    risco = models.CharField(max_length=20, default="baixo")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA)
    data_reagendamento = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = EmpresaScopedManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["prioridade", "-valor_potencial"]
        db_table = '"crm"."oportunidade_tb"'
        indexes = [
            models.Index(fields=["status", "prioridade"], name="oportunidade_status_idx"),
            models.Index(fields=["empresa", "status"], name="oportunidade_empresa_idx"),
        ]

    def __str__(self):
        return f"{self.tipo} - {self.cliente}"
