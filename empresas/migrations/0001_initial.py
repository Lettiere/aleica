from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            """
            CREATE SCHEMA IF NOT EXISTS core;
            CREATE SCHEMA IF NOT EXISTS crm;
            CREATE SCHEMA IF NOT EXISTS cliente;
            CREATE SCHEMA IF NOT EXISTS contrato;
            CREATE SCHEMA IF NOT EXISTS financeiro;
            CREATE SCHEMA IF NOT EXISTS documento;
            CREATE SCHEMA IF NOT EXISTS relatorio;
            CREATE SCHEMA IF NOT EXISTS auditoria;
            CREATE OR REPLACE FUNCTION core.fn_set_updated_at()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.CreateModel(
            name="Empresa",
            fields=[
                ("empresa_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("razao_social", models.CharField(blank=True, max_length=190)),
                ("nome_fantasia", models.CharField(max_length=160)),
                ("cnpj", models.CharField(blank=True, max_length=24)),
                ("email", models.EmailField(blank=True, max_length=180)),
                ("telefone", models.CharField(blank=True, max_length=30)),
                ("status", models.CharField(choices=[("ativa", "Ativa"), ("inativa", "Inativa"), ("prospect", "Prospect")], default="ativa", max_length=20)),
                ("segmento", models.CharField(blank=True, max_length=100)),
                ("cidade", models.CharField(blank=True, max_length=100)),
                ("estado", models.CharField(blank=True, max_length=2)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={"ordering": ["nome_fantasia"], "db_table": '"core"."empresa_tb"'},
        ),
    ]
