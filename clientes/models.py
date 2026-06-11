from django.db import models

from core.managers import EmpresaScopedManager
from empresas.models import Empresa


class Cliente(models.Model):
    class Status(models.TextChoices):
        ATIVO = "ativo", "Ativo"
        VIP = "vip", "VIP"
        RECORRENTE = "recorrente", "Recorrente"
        INATIVO = "inativo", "Inativo"
        PERDIDO = "perdido", "Perdido"
        REATIVADO = "reativado", "Reativado"
        ORCAMENTO_ABANDONADO = "orcamento_abandonado", "Orcamento abandonado"
        POS_VENDA_PENDENTE = "pos_venda_pendente", "Pos-venda pendente"

    cliente_id = models.BigAutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column="empresa_id_fk", related_name="clientes")
    nome = models.CharField(max_length=160)
    cnpj = models.CharField(max_length=24, blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=180, blank=True)
    origem = models.CharField(max_length=80, blank=True)
    ultimo_atendimento = models.DateField(null=True, blank=True)
    valor_total_gasto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantidade_compras = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=40, choices=Status.choices, default=Status.ATIVO)
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = EmpresaScopedManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["ultimo_atendimento", "nome"]
        db_table = '"cliente"."cliente_tb"'
        indexes = [
            models.Index(fields=["cnpj"], name="cliente_cnpj_idx"),
            models.Index(fields=["status"], name="cliente_status_idx"),
            models.Index(fields=["ultimo_atendimento"], name="cliente_ultimo_atend_idx"),
            models.Index(fields=["empresa", "status"], name="cliente_empresa_status_idx"),
        ]

    def __str__(self):
        return self.nome
