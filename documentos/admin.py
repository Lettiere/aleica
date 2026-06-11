from django.contrib import admin

from documentos.models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "categoria", "created_at", "ativo")
    list_filter = ("categoria", "ativo", "empresa")
    search_fields = ("titulo", "categoria", "empresa__nome_fantasia")
