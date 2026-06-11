import csv
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from clientes.forms import ClienteForm
from clientes.models import Cliente
from inteligencia.services import gerar_oportunidades


@login_required
def cliente_list(request):
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    qs = Cliente.objects.select_related("empresa").filter(ativo=True)
    if q:
        qs = qs.filter(Q(nome__icontains=q) | Q(cnpj__icontains=q) | Q(email__icontains=q) | Q(telefone__icontains=q) | Q(empresa__nome_fantasia__icontains=q))
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
    cliente = get_object_or_404(Cliente, pk=pk, ativo=True) if pk else None
    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == "POST" and form.is_valid():
        cliente = form.save()
        gerar_oportunidades(cliente)
        return redirect("clientes_list")
    return render(request, "clientes/form.html", {"form": form, "cliente": cliente, "title": "Cliente"})


@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, ativo=True)
    if request.method == "POST":
        cliente.ativo = False
        cliente.deleted_at = timezone.now()
        cliente.save(update_fields=["ativo", "deleted_at", "updated_at"])
        messages.success(request, "Cliente excluido da operacao.")
        return redirect("clientes_list")
    return render(request, "core/confirm_delete.html", {"object": cliente, "title": "Excluir cliente", "cancel_url": "clientes_detail"})


@login_required
def cliente_import(request):
    if request.method == "POST" and request.FILES.get("arquivo"):
        arquivo = request.FILES["arquivo"].read().decode("utf-8-sig").splitlines()
        reader = csv.DictReader(arquivo)
        criados = 0
        for row in reader:
            form = ClienteForm({
                "empresa": row.get("empresa") or row.get("empresa_id") or getattr(request.empresa, "pk", ""),
                "nome": row.get("nome", ""),
                "cnpj": row.get("cnpj", ""),
                "telefone": row.get("telefone", ""),
                "whatsapp": row.get("whatsapp", ""),
                "email": row.get("email", ""),
                "origem": row.get("origem", "Importacao"),
                "ultimo_atendimento": row.get("ultimo_atendimento", ""),
                "valor_total_gasto": row.get("valor_total_gasto", 0) or 0,
                "quantidade_compras": row.get("quantidade_compras", 0) or 0,
                "status": row.get("status", Cliente.Status.ATIVO),
                "observacoes": row.get("observacoes", ""),
            })
            if form.is_valid():
                cliente = form.save()
                gerar_oportunidades(cliente)
                criados += 1
        messages.success(request, f"{criados} clientes importados.")
        return redirect("clientes_list")
    return render(request, "clientes/import.html", {"title": "Importar clientes"})


@login_required
def buscar_cnpj(request):
    cnpj = "".join(filter(str.isdigit, request.GET.get("cnpj", "")))
    if len(cnpj) != 14:
        return JsonResponse({"ok": False, "erro": "Informe um CNPJ com 14 digitos."}, status=400)
    try:
        with urlopen(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}", timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        return JsonResponse({"ok": False, "erro": f"BrasilAPI retornou HTTP {exc.code}."}, status=exc.code)
    except URLError:
        return JsonResponse({"ok": False, "erro": "BrasilAPI indisponivel no momento."}, status=503)
    return JsonResponse({
        "ok": True,
        "nome": data.get("razao_social") or data.get("nome_fantasia") or "",
        "email": data.get("email") or "",
        "telefone": data.get("ddd_telefone_1") or "",
        "cidade": data.get("municipio") or "",
        "estado": data.get("uf") or "",
        "raw": data,
    })
