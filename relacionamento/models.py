from django.conf import settings
from django.db import models

from clientes.models import Cliente
from oportunidades.models import Oportunidade


class HistoricoContato(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="historicos")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    oportunidade = models.ForeignKey(Oportunidade, null=True, blank=True, on_delete=models.SET_NULL, related_name="historicos")
    data_contato = models.DateTimeField()
    tipo_contato = models.CharField(max_length=80)
    resultado = models.CharField(max_length=160)
    observacao = models.TextField(blank=True)
    proxima_acao = models.CharField(max_length=160, blank=True)
    data_proxima_acao = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_contato"]

    def __str__(self):
        return f"{self.cliente} - {self.tipo_contato}"
