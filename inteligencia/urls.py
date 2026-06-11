from django.urls import path

from inteligencia import views


urlpatterns = [
    path("", views.inteligencia, name="inteligencia"),
]
