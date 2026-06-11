from core.tenant import clear_current_context, perfil_codigo, set_current_empresa, set_current_perfil


class EmpresaContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        clear_current_context()
        request.empresa = None
        request.perfil_codigo = None
        user = getattr(request, "user", None)
        if getattr(user, "is_authenticated", False):
            perfil = perfil_codigo(user)
            usuario_saas = getattr(user, "usuario_saas", None)
            empresa = getattr(usuario_saas, "empresa", None)
            request.empresa = empresa
            request.perfil_codigo = perfil
            set_current_empresa(empresa)
            set_current_perfil(perfil)
        try:
            return self.get_response(request)
        finally:
            clear_current_context()

