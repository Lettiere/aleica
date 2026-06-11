from django.contrib import admin

from inteligencia.models import SnapshotInteligencia


@admin.register(SnapshotInteligencia)
class SnapshotInteligenciaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "score_aleica", "risco", "probabilidade_perda", "valor_potencial", "criado_em")
    list_filter = ("risco",)
