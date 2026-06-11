from django.db import models

from clientes.models import Cliente
from core.managers import EmpresaScopedManager
from empresas.models import Empresa


class SnapshotInteligencia(models.Model):
    snapshot_inteligencia_id = models.BigAutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column="empresa_id_fk", related_name="snapshots_inteligencia")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column="cliente_id_fk", related_name="snapshots_inteligencia")
    score_aleica = models.PositiveIntegerField(default=0)
    risco = models.CharField(max_length=20)
    probabilidade_perda = models.PositiveIntegerField(default=0)
    dias_sem_retorno = models.PositiveIntegerField(default=0)
    valor_potencial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    motivo_alerta = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = EmpresaScopedManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["-created_at"]
        db_table = '"relatorio"."snapshot_inteligencia_tb"'

    def __str__(self):
        return f"{self.cliente} - {self.score_aleica}"
