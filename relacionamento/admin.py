from django.contrib import admin

from relacionamento.models import HistoricoContato


@admin.register(HistoricoContato)
class HistoricoContatoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "usuario", "data_contato", "tipo_contato", "resultado")
    search_fields = ("cliente__nome", "resultado", "observacao")
    list_filter = ("tipo_contato", "resultado")
