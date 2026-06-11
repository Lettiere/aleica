import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("clientes", "0001_initial"), ("empresas", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Oportunidade",
            fields=[
                ("oportunidade_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("tipo", models.CharField(max_length=90)),
                ("prioridade", models.CharField(choices=[("baixo", "Baixo"), ("medio", "Medio"), ("alto", "Alto"), ("critico", "Critico")], default="baixo", max_length=20)),
                ("score", models.PositiveIntegerField(default=0)),
                ("probabilidade_perda", models.PositiveIntegerField(default=0)),
                ("valor_potencial", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("motivo", models.CharField(max_length=255)),
                ("descricao", models.TextField(blank=True)),
                ("acao_sugerida", models.CharField(max_length=255)),
                ("risco", models.CharField(default="baixo", max_length=20)),
                ("status", models.CharField(choices=[("aberta", "Aberta"), ("em_andamento", "Em andamento"), ("concluida", "Concluida"), ("perdida", "Perdida")], default="aberta", max_length=20)),
                ("data_reagendamento", models.DateField(blank=True, null=True)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("cliente", models.ForeignKey(db_column="cliente_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="oportunidades", to="clientes.cliente")),
                ("empresa", models.ForeignKey(db_column="empresa_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="oportunidades", to="empresas.empresa")),
            ],
            options={
                "ordering": ["prioridade", "-valor_potencial"],
                "db_table": '"crm"."oportunidade_tb"',
                "indexes": [models.Index(fields=["status", "prioridade"], name="oportunidade_status_idx"), models.Index(fields=["empresa", "status"], name="oportunidade_empresa_idx")],
            },
        ),
    ]
