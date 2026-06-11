from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from clientes.forms import ClienteForm
from clientes.models import Cliente
from inteligencia.services import gerar_oportunidades


@login_required
def cliente_list(request):
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    qs = Cliente.objects.select_related("empresa")
    if q:
        qs = qs.filter(Q(nome__icontains=q) | Q(email__icontains=q) | Q(telefone__icontains=q) | Q(empresa__nome_fantasia__icontains=q))
    if status:
        qs = qs.filter(status=status)
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    return render(request, "clientes/list.html", {"page_obj": page, "q": q, "status": status, "title": "Clientes"})


@login_required
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente.objects.select_related("empresa"), pk=pk)
    return render(request, "clientes/detail.html", {"cliente": cliente, "title": cliente.nome})


@login_required
def cliente_form(request, pk=None):
    cliente = get_object_or_404(Cliente, pk=pk) if pk else None
    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == "POST" and form.is_valid():
        cliente = form.save()
        gerar_oportunidades(cliente)
        return redirect("clientes_list")
    return render(request, "clientes/form.html", {"form": form, "cliente": cliente, "title": "Cliente"})
