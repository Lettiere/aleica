from django.urls import path

from dashboards import views


urlpatterns = [
    path("assessoria/", views.assessoria_dashboard, name="assessoria_dashboard"),
    path("cliente/", views.cliente_dashboard, name="cliente_dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("relatorios/", views.relatorios, name="relatorios"),
    path("relatorios/exportar-clientes/", views.exportar_clientes, name="relatorios_exportar_clientes"),
]
