import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("clientes", "0001_initial"),
        ("empresas", "0001_initial"),
        ("oportunidades", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricoContato",
            fields=[
                ("historico_contato_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("data_contato", models.DateTimeField()),
                ("tipo_contato", models.CharField(max_length=80)),
                ("resultado", models.CharField(max_length=160)),
                ("observacao", models.TextField(blank=True)),
                ("proxima_acao", models.CharField(blank=True, max_length=160)),
                ("data_proxima_acao", models.DateField(blank=True, null=True)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("cliente", models.ForeignKey(db_column="cliente_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="historicos", to="clientes.cliente")),
                ("empresa", models.ForeignKey(db_column="empresa_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="historicos_contato", to="empresas.empresa")),
                ("oportunidade", models.ForeignKey(blank=True, db_column="oportunidade_id_fk", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="historicos", to="oportunidades.oportunidade")),
                ("usuario", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-data_contato"], "db_table": '"crm"."historico_contato_tb"'},
        ),
    ]
