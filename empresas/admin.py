from django.contrib import admin

from empresas.models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome_fantasia", "segmento", "cidade", "status")
    search_fields = ("nome_fantasia", "razao_social", "cnpj", "segmento")
    list_filter = ("status", "segmento", "estado")
