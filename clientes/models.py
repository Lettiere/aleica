from django.db import models

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

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="clientes")
    nome = models.CharField(max_length=160)
    telefone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=180, blank=True)
    origem = models.CharField(max_length=80, blank=True)
    ultimo_atendimento = models.DateField(null=True, blank=True)
    valor_total_gasto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantidade_compras = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=40, choices=Status.choices, default=Status.ATIVO)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ultimo_atendimento", "nome"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["ultimo_atendimento"]),
            models.Index(fields=["empresa", "status"]),
        ]

    def __str__(self):
        return self.nome
