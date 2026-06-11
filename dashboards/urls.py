from django.urls import path

from dashboards import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("relatorios/", views.relatorios, name="relatorios"),
]
