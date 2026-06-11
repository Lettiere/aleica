from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("empresas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Documento",
            fields=[
                ("documento_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("titulo", models.CharField(max_length=180)),
                ("categoria", models.CharField(blank=True, max_length=80)),
                ("arquivo", models.FileField(upload_to="documentos/%Y/%m/")),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("empresa", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="documentos", to="empresas.empresa")),
            ],
            options={
                "ordering": ["categoria", "-created_at"],
            },
        ),
    ]
