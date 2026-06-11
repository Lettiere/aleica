from django.db import models

from clientes.models import Cliente


class SnapshotInteligencia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="snapshots_inteligencia")
    score_aleica = models.PositiveIntegerField(default=0)
    risco = models.CharField(max_length=20)
    probabilidade_perda = models.PositiveIntegerField(default=0)
    dias_sem_retorno = models.PositiveIntegerField(default=0)
    valor_potencial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    motivo_alerta = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.cliente} - {self.score_aleica}"
