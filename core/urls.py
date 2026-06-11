from django.urls import path

from core import views


urlpatterns = [
    path("usuarios/", views.usuario_list, name="usuarios_list"),
    path("usuarios/novo/", views.usuario_form, name="usuarios_create"),
    path("usuarios/<int:pk>/editar/", views.usuario_form, name="usuarios_update"),
    path("usuarios/<int:pk>/status/", views.usuario_toggle, name="usuarios_toggle"),
    path("perfis/", views.perfil_list, name="perfis_list"),
    path("perfis/novo/", views.perfil_form, name="perfis_create"),
    path("perfis/<int:pk>/editar/", views.perfil_form, name="perfis_update"),
    path("permissoes/", views.permissao_list, name="permissoes_list"),
    path("permissoes/nova/", views.permissao_form, name="permissoes_create"),
    path("permissoes/<int:pk>/editar/", views.permissao_form, name="permissoes_update"),
]
