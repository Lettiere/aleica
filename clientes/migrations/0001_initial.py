import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("empresas", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                ("cliente_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=160)),
                ("telefone", models.CharField(blank=True, max_length=30)),
                ("whatsapp", models.CharField(blank=True, max_length=30)),
                ("email", models.EmailField(blank=True, max_length=180)),
                ("origem", models.CharField(blank=True, max_length=80)),
                ("ultimo_atendimento", models.DateField(blank=True, null=True)),
                ("valor_total_gasto", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("quantidade_compras", models.PositiveIntegerField(default=0)),
                ("status", models.CharField(choices=[("ativo", "Ativo"), ("vip", "VIP"), ("recorrente", "Recorrente"), ("inativo", "Inativo"), ("perdido", "Perdido"), ("reativado", "Reativado"), ("orcamento_abandonado", "Orcamento abandonado"), ("pos_venda_pendente", "Pos-venda pendente")], default="ativo", max_length=40)),
                ("observacoes", models.TextField(blank=True)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("empresa", models.ForeignKey(db_column="empresa_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="clientes", to="empresas.empresa")),
            ],
            options={
                "ordering": ["ultimo_atendimento", "nome"],
                "db_table": '"cliente"."cliente_tb"',
                "indexes": [models.Index(fields=["status"], name="cliente_status_idx"), models.Index(fields=["ultimo_atendimento"], name="cliente_ultimo_atend_idx"), models.Index(fields=["empresa", "status"], name="cliente_empresa_status_idx")],
            },
        ),
    ]
