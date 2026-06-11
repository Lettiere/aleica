from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="cnpj",
            field=models.CharField(blank=True, max_length=24),
        ),
        migrations.AddIndex(
            model_name="cliente",
            index=models.Index(fields=["cnpj"], name="cliente_cnpj_idx"),
        ),
    ]
