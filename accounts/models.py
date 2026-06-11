from django.conf import settings
from django.db import models


class PerfilUsuario(models.Model):
    class Perfil(models.TextChoices):
        MASTER = "MASTER", "Master"
        GESTORA_RELACIONAMENTO = "GESTORA_RELACIONAMENTO", "Gestora de Relacionamento"
        ANALISTA = "ANALISTA", "Analista"

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_aleica")
    perfil = models.CharField(max_length=40, choices=Perfil.choices, default=Perfil.ANALISTA)
    telefone = models.CharField(max_length=30, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.get_perfil_display()}"
