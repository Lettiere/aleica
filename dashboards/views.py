import csv

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render

from clientes.models import Cliente
from core.rbac import permission_required
from empresas.models import Empresa
from oportunidades.models import Oportunidade
from relacionamento.models import HistoricoContato


def _dashboard_metrics():
    abertas = Oportunidade.objects.filter(status__in=[Oportunidade.Status.ABERTA, Oportunidade.Status.EM_ANDAMENTO])
    return abertas, {
        "empresas": Empresa.objects.count(),
        "clientes": Cliente.objects.count(),
        "ativos": Cliente.objects.filter(status__in=["ativo", "vip", "recorrente", "reativado"]).count(),
        "inativos": Cliente.objects.filter(status__in=["inativo", "perdido"]).count(),
        "risco": abertas.filter(prioridade__in=["alto", "critico"]).count(),
        "oportunidades": abertas.count(),
        "receita": abertas.aggregate(total=Sum("valor_potencial"))["total"] or 0,
        "contatos": HistoricoContato.objects.count(),
    }


@permission_required("assessoria:dashboard")
def dashboard(request):
    abertas, metrics = _dashboard_metrics()
    charts = {
        "status": list(Cliente.objects.values("status").annotate(total=Count("pk")).order_by("-total")),
        "risco": list(abertas.values("risco").annotate(total=Count("pk")).order_by("risco")),
        "empresas": list(Empresa.objects.annotate(total=Count("oportunidades")).values("nome_fantasia", "total")[:8]),
        "contatos": list(
            HistoricoContato.objects.annotate(month=TruncMonth("data_contato"))
            .values("month")
            .annotate(total=Count("pk"))
            .order_by("month")[:12]
        ),
    }
    return render(request, "dashboards/dashboard.html", {"metrics": metrics, "charts": charts, "title": "Dashboard Executivo"})


@permission_required("assessoria:dashboard")
def assessoria_dashboard(request):
    _, metrics = _dashboard_metrics()
    return render(request, "dashboards/assessoria.html", {"metrics": metrics, "title": "Dashboard da Assessoria"})


@permission_required("cliente:dashboard")
def cliente_dashboard(request):
    _, metrics = _dashboard_metrics()
    return render(request, "dashboards/cliente.html", {"metrics": metrics, "title": "Dashboard do Cliente"})


@permission_required("relatorio:read")
def relatorios(request):
    abertas = Oportunidade.objects.filter(status=Oportunidade.Status.ABERTA).select_related("cliente", "empresa")
    reports = {
        "Clientes em risco": abertas.filter(prioridade__in=["alto", "critico"]).order_by("-valor_potencial")[:12],
        "Clientes inativos": Cliente.objects.filter(status__in=["inativo", "perdido"]).select_related("empresa").order_by("-valor_total_gasto")[:12],
        "Clientes VIP": Cliente.objects.filter(valor_total_gasto__gte=8000).select_related("empresa").order_by("-valor_total_gasto")[:12],
        "Receita potencial": abertas.order_by("-valor_potencial")[:12],
        "Acoes realizadas": HistoricoContato.objects.select_related("cliente", "cliente__empresa").order_by("-data_contato")[:12],
        "Oportunidades por segmento": abertas.values("empresa__segmento").annotate(total=Count("pk"), receita=Sum("valor_potencial")).order_by("-receita"),
    }
    return render(request, "relatorios/index.html", {"reports": reports, "title": "Relatorios"})


@permission_required("relatorio:read")
def exportar_clientes(request):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="clientes_aleica.csv"'
    writer = csv.writer(response)
    writer.writerow(["empresa", "nome", "cnpj", "telefone", "whatsapp", "email", "status", "ultimo_atendimento", "valor_total_gasto", "quantidade_compras"])
    for cliente in Cliente.objects.select_related("empresa").filter(ativo=True):
        writer.writerow([
            cliente.empresa.nome_fantasia,
            cliente.nome,
            cliente.cnpj,
            cliente.telefone,
            cliente.whatsapp,
            cliente.email,
            cliente.status,
            cliente.ultimo_atendimento or "",
            cliente.valor_total_gasto,
            cliente.quantidade_compras,
        ])
    return response
