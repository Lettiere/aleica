from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


PERMISSOES_POR_PERFIL = {
    "ROOT": {"*"},
    "ADMIN_ASSESSORIA": {"assessoria:*", "cliente:*", "crm:*", "financeiro:*", "contrato:*", "relatorio:*"},
    "GESTOR": {"assessoria:dashboard", "crm:*", "relatorio:*", "cliente:*"},
    "OPERADOR": {"assessoria:dashboard", "crm:*", "relacionamento:*"},
    "CLIENTE_ADMIN": {"cliente:*", "documento:*", "solicitacao:*", "relatorio:*", "contrato:*", "atendimento:*"},
    "CLIENTE_USUARIO": {"cliente:dashboard", "documento:read", "solicitacao:*", "relatorio:read", "contrato:read", "atendimento:*"},
}


def has_permission(perfil, codigo):
    permissoes = PERMISSOES_POR_PERFIL.get(perfil, set())
    prefixo = codigo.split(":", 1)[0] + ":*"
    return "*" in permissoes or codigo in permissoes or prefixo in permissoes


def permission_required(codigo):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            if not has_permission(getattr(request, "perfil_codigo", None), codigo):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator

