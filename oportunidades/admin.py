from django.contrib import admin

from oportunidades.models import Oportunidade


@admin.register(Oportunidade)
class OportunidadeAdmin(admin.ModelAdmin):
    list_display = ("cliente", "empresa", "tipo", "prioridade", "probabilidade_perda", "valor_potencial", "status")
    search_fields = ("cliente__nome", "empresa__nome_fantasia", "tipo", "motivo")
    list_filter = ("prioridade", "status", "tipo", "risco")
