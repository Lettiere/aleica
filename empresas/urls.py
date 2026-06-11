from django.urls import path

from empresas import views


urlpatterns = [
    path("", views.empresa_list, name="empresas_list"),
    path("nova/", views.empresa_form, name="empresas_create"),
    path("<int:pk>/", views.empresa_detail, name="empresas_detail"),
    path("<int:pk>/editar/", views.empresa_form, name="empresas_update"),
]
