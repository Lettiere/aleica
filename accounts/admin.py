from django.contrib import admin

from accounts.models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "perfil", "telefone")
    list_filter = ("perfil",)
