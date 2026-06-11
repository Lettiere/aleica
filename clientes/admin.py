from django.contrib import admin

from clientes.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "empresa", "status", "ultimo_atendimento", "valor_total_gasto", "quantidade_compras")
    search_fields = ("nome", "email", "telefone", "whatsapp", "empresa__nome_fantasia")
    list_filter = ("status", "origem", "empresa")
