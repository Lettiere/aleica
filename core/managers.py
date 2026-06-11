from django.db import models

from core.tenant import get_current_empresa, get_current_perfil, perfil_acessa_todas_empresas


class EmpresaScopedQuerySet(models.QuerySet):
    def for_request(self, request):
        empresa = getattr(request, "empresa", None)
        perfil = getattr(request, "perfil_codigo", None)
        if empresa and not perfil_acessa_todas_empresas(perfil):
            return self.filter(empresa=empresa)
        return self


class EmpresaScopedManager(models.Manager.from_queryset(EmpresaScopedQuerySet)):
    def get_queryset(self):
        qs = super().get_queryset()
        empresa = get_current_empresa()
        perfil = get_current_perfil()
        if empresa and not perfil_acessa_todas_empresas(perfil):
            return qs.filter(empresa=empresa)
        return qs


class EmpresaRootScopedQuerySet(models.QuerySet):
    def for_request(self, request):
        empresa = getattr(request, "empresa", None)
        perfil = getattr(request, "perfil_codigo", None)
        if empresa and not perfil_acessa_todas_empresas(perfil):
            return self.filter(pk=empresa.pk)
        return self


class EmpresaRootScopedManager(models.Manager.from_queryset(EmpresaRootScopedQuerySet)):
    def get_queryset(self):
        qs = super().get_queryset()
        empresa = get_current_empresa()
        perfil = get_current_perfil()
        if empresa and not perfil_acessa_todas_empresas(perfil):
            return qs.filter(pk=empresa.pk)
        return qs

