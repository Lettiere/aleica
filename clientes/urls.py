from django.urls import path

from clientes import views


urlpatterns = [
    path("", views.cliente_list, name="clientes_list"),
    path("novo/", views.cliente_form, name="clientes_create"),
    path("<int:pk>/", views.cliente_detail, name="clientes_detail"),
    path("<int:pk>/editar/", views.cliente_form, name="clientes_update"),
]
