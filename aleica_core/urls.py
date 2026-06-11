from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from website.views import LandingPageView


urlpatterns = [
    path("", LandingPageView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("dashboards.urls")),
    path("empresas/", include("empresas.urls")),
    path("clientes/", include("clientes.urls")),
    path("oportunidades/", include("oportunidades.urls")),
    path("relacionamento/", include("relacionamento.urls")),
    path("inteligencia/", include("inteligencia.urls")),
]
