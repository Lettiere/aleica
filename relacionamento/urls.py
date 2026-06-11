from django.urls import path

from relacionamento import views


urlpatterns = [
    path("fila/", views.fila_carine, name="fila_carine"),
    path("historico/", views.historico, name="historico_contatos"),
    path("contato/novo/", views.contato_form, name="contato_create"),
    path("fila/<int:pk>/contatado/", views.marcar_contatado, name="fila_contatado"),
    path("fila/<int:pk>/reagendar/", views.reagendar, name="fila_reagendar"),
]
