from django.urls import path

from documentos import views


urlpatterns = [
    path("", views.documento_list, name="documentos_list"),
    path("upload/", views.documento_upload, name="documentos_upload"),
    path("<int:pk>/download/", views.documento_download, name="documentos_download"),
]
