from django.db import models

from empresas.models import Empresa


class Documento(models.Model):
    documento_id = models.BigAutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="documentos")
    titulo = models.CharField(max_length=180)
    categoria = models.CharField(max_length=80, blank=True)
    arquivo = models.FileField(upload_to="documentos/%Y/%m/")
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["categoria", "-created_at"]

    def __str__(self):
        return self.titulo
