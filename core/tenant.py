from threading import local


_state = local()

ASSESSORIA_PERFIS = {"ROOT", "ADMIN_ASSESSORIA", "GESTOR", "OPERADOR"}
CLIENTE_PERFIS = {"CLIENTE_ADMIN", "CLIENTE_USUARIO"}


def set_current_empresa(empresa):
    _state.empresa = empresa


def get_current_empresa():
    return getattr(_state, "empresa", None)


def set_current_perfil(perfil):
    _state.perfil = perfil


def get_current_perfil():
    return getattr(_state, "perfil", None)


def clear_current_context():
    _state.empresa = None
    _state.perfil = None


def perfil_codigo(user):
    if not getattr(user, "is_authenticated", False):
        return None
    if getattr(user, "is_superuser", False):
        return "ROOT"
    usuario_saas = getattr(user, "usuario_saas", None)
    if usuario_saas and usuario_saas.perfil_id:
        return usuario_saas.perfil.nome_perfil
    perfil_aleica = getattr(user, "perfil_aleica", None)
    if perfil_aleica:
        legado = {
            "MASTER": "ROOT",
            "GESTORA_RELACIONAMENTO": "OPERADOR",
            "ANALISTA": "GESTOR",
        }
        return legado.get(perfil_aleica.perfil, "GESTOR")
    return None


def perfil_acessa_todas_empresas(perfil):
    return perfil in ASSESSORIA_PERFIS

