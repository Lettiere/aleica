import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("empresas", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Perfil",
            fields=[
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("perfil_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("nome_perfil", models.CharField(choices=[("ROOT", "Root"), ("ADMIN_ASSESSORIA", "Admin Assessoria"), ("GESTOR", "Gestor"), ("OPERADOR", "Operador"), ("CLIENTE_ADMIN", "Cliente Admin"), ("CLIENTE_USUARIO", "Cliente Usuario")], max_length=40, unique=True)),
                ("descricao", models.CharField(blank=True, max_length=255)),
            ],
            options={"db_table": '"core"."perfil_tb"'},
        ),
        migrations.CreateModel(
            name="Permissao",
            fields=[
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("permissao_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo", models.CharField(max_length=80, unique=True)),
                ("descricao", models.CharField(blank=True, max_length=255)),
            ],
            options={"db_table": '"core"."permissao_tb"'},
        ),
        migrations.CreateModel(
            name="Usuario",
            fields=[
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("usuario_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=160)),
                ("email", models.EmailField(max_length=180, unique=True)),
                ("senha_hash", models.CharField(max_length=255)),
                ("ultimo_login", models.DateTimeField(blank=True, null=True)),
                ("auth_user", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="usuario_saas", to=settings.AUTH_USER_MODEL)),
                ("empresa", models.ForeignKey(blank=True, db_column="empresa_id_fk", null=True, on_delete=django.db.models.deletion.PROTECT, related_name="usuarios", to="empresas.empresa")),
                ("perfil", models.ForeignKey(db_column="perfil_id_fk", on_delete=django.db.models.deletion.PROTECT, related_name="usuarios", to="core.perfil")),
            ],
            options={"db_table": '"core"."usuario_tb"'},
        ),
        migrations.CreateModel(
            name="UsuarioPermissao",
            fields=[
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("usuario_permissao_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("permissao", models.ForeignKey(db_column="permissao_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="usuarios_permissao", to="core.permissao")),
                ("usuario", models.ForeignKey(db_column="usuario_id_fk", on_delete=django.db.models.deletion.CASCADE, related_name="permissoes_usuario", to="core.usuario")),
            ],
            options={"db_table": '"core"."usuario_permissao_tb"'},
        ),
        migrations.AddConstraint("perfil", models.UniqueConstraint(fields=("nome_perfil",), name="perfil_nome_perfil_uk")),
        migrations.AddConstraint("permissao", models.UniqueConstraint(fields=("codigo",), name="permissao_codigo_uk")),
        migrations.AddConstraint("usuario", models.UniqueConstraint(fields=("email",), name="usuario_email_uk")),
        migrations.AddConstraint("usuariopermissao", models.UniqueConstraint(fields=("usuario", "permissao"), name="usuario_permissao_usuario_permissao_uk")),
    ]
