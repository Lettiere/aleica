import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("clientes", "0001_initial"), ("empresas", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="SnapshotInteligencia",
            fields=[
                ("snapshot_inteligencia_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("score_aleica", models.PositiveIntegerField(default=0)),
                ("risco", models.CharField(max_length=20)),
                ("probabilidade_perda", models.PositiveIntegerField(default=0)),
                ("dias_sem_retorno", models.PositiveIntegerField(default=0)),
                ("valor_potencial", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("motivo_alerta", models.CharField(max_length=255)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("cliente", models.ForeignKey(db_column="cliente_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="snapshots_inteligencia", to="clientes.cliente")),
                ("empresa", models.ForeignKey(db_column="empresa_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="snapshots_inteligencia", to="empresas.empresa")),
            ],
            options={"ordering": ["-created_at"], "db_table": '"relatorio"."snapshot_inteligencia_tb"'},
        ),
    ]
