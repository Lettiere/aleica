from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import PerfilForm, PermissaoForm, UsuarioForm
from core.models import Perfil, Permissao, Usuario


@login_required
def usuario_list(request):
    q = request.GET.get("q", "")
    qs = Usuario.objects.select_related("auth_user", "empresa", "perfil").order_by("nome")
    if q:
        qs = qs.filter(nome__icontains=q) | qs.filter(email__icontains=q)
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    return render(request, "core/usuarios/list.html", {"page_obj": page, "q": q, "title": "Usuarios"})


@login_required
def usuario_form(request, pk=None):
    usuario = get_object_or_404(Usuario, pk=pk) if pk else None
    form = UsuarioForm(request.POST or None, instance=usuario)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario salvo e sincronizado com a autenticacao Django.")
        return redirect("usuarios_list")
    return render(request, "core/usuarios/form.html", {"form": form, "usuario": usuario, "title": "Usuario"})


@login_required
def usuario_toggle(request, pk):
    usuario = get_object_or_404(Usuario.objects.select_related("auth_user"), pk=pk)
    if request.method == "POST":
        usuario.ativo = not usuario.ativo
        usuario.save(update_fields=["ativo", "updated_at"])
        if usuario.auth_user:
            usuario.auth_user.is_active = usuario.ativo
            usuario.auth_user.save(update_fields=["is_active"])
        messages.success(request, "Status do usuario atualizado.")
    return redirect("usuarios_list")


@login_required
def perfil_list(request):
    page = Paginator(Perfil.objects.order_by("nome_perfil"), 20).get_page(request.GET.get("page"))
    return render(request, "core/perfis/list.html", {"page_obj": page, "title": "Perfis"})


@login_required
def perfil_form(request, pk=None):
    perfil = get_object_or_404(Perfil, pk=pk) if pk else None
    form = PerfilForm(request.POST or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("perfis_list")
    return render(request, "core/perfis/form.html", {"form": form, "perfil": perfil, "title": "Perfil"})


@login_required
def permissao_list(request):
    page = Paginator(Permissao.objects.order_by("codigo"), 20).get_page(request.GET.get("page"))
    return render(request, "core/permissoes/list.html", {"page_obj": page, "title": "Permissoes"})


@login_required
def permissao_form(request, pk=None):
    permissao = get_object_or_404(Permissao, pk=pk) if pk else None
    form = PermissaoForm(request.POST or None, instance=permissao)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("permissoes_list")
    return render(request, "core/permissoes/form.html", {"form": form, "permissao": permissao, "title": "Permissao"})
