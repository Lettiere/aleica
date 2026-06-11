from django.conf import settings
from django.db import models

from clientes.models import Cliente
from core.managers import EmpresaScopedManager
from empresas.models import Empresa
from oportunidades.models import Oportunidade


class HistoricoContato(models.Model):
    historico_contato_id = models.BigAutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column="empresa_id_fk", related_name="historicos_contato")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column="cliente_id_fk", related_name="historicos")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    oportunidade = models.ForeignKey(Oportunidade, null=True, blank=True, on_delete=models.SET_NULL, db_column="oportunidade_id_fk", related_name="historicos")
    data_contato = models.DateTimeField()
    tipo_contato = models.CharField(max_length=80)
    resultado = models.CharField(max_length=160)
    observacao = models.TextField(blank=True)
    proxima_acao = models.CharField(max_length=160, blank=True)
    data_proxima_acao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = EmpresaScopedManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["-data_contato"]
        db_table = '"crm"."historico_contato_tb"'

    def __str__(self):
        return f"{self.cliente} - {self.tipo_contato}"
