from django.urls import path

from oportunidades import views


urlpatterns = [
    path("", views.oportunidade_list, name="oportunidades_list"),
    path("<int:pk>/", views.oportunidade_detail, name="oportunidades_detail"),
    path("<int:pk>/status/<str:status>/", views.oportunidade_status, name="oportunidades_status"),
]
