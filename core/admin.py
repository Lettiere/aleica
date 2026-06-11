from django.contrib import admin

from core.models import Perfil, Permissao, Usuario, UsuarioPermissao


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("nome_perfil", "descricao", "ativo")
    search_fields = ("nome_perfil", "descricao")
    list_filter = ("ativo",)


@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descricao", "ativo")
    search_fields = ("codigo", "descricao")
    list_filter = ("ativo",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "empresa", "perfil", "ativo")
    search_fields = ("nome", "email", "empresa__nome_fantasia")
    list_filter = ("perfil", "ativo")


@admin.register(UsuarioPermissao)
class UsuarioPermissaoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "permissao", "ativo")
    search_fields = ("usuario__nome", "permissao__codigo")
    list_filter = ("ativo",)
