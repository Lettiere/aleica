from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from empresas.forms import EmpresaForm
from empresas.models import Empresa


@login_required
def empresa_list(request):
    q = request.GET.get("q", "")
    qs = Empresa.objects.filter(ativo=True)
    if q:
        qs = qs.filter(nome_fantasia__icontains=q) | qs.filter(segmento__icontains=q) | qs.filter(cidade__icontains=q)
    page = Paginator(qs, 15).get_page(request.GET.get("page"))
    return render(request, "empresas/list.html", {"page_obj": page, "q": q, "title": "Empresas"})


@login_required
def empresa_detail(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk, ativo=True)
    return render(request, "empresas/detail.html", {"empresa": empresa, "title": empresa.nome_fantasia})


@login_required
def empresa_form(request, pk=None):
    empresa = get_object_or_404(Empresa, pk=pk, ativo=True) if pk else None
    form = EmpresaForm(request.POST or None, instance=empresa)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("empresas_list")
    return render(request, "empresas/form.html", {"form": form, "empresa": empresa, "title": "Empresa"})


@login_required
def empresa_delete(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk, ativo=True)
    if request.method == "POST":
        empresa.ativo = False
        empresa.deleted_at = timezone.now()
        empresa.save(update_fields=["ativo", "deleted_at", "updated_at"])
        messages.success(request, "Empresa excluida da operacao.")
        return redirect("empresas_list")
    return render(request, "core/confirm_delete.html", {"object": empresa, "title": "Excluir empresa", "cancel_url": "empresas_detail"})
