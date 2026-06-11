from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from clientes.models import Cliente
from empresas.models import Empresa
from oportunidades.models import Oportunidade
from relacionamento.models import HistoricoContato


@login_required
def dashboard(request):
    abertas = Oportunidade.objects.filter(status__in=[Oportunidade.Status.ABERTA, Oportunidade.Status.EM_ANDAMENTO])
    metrics = {
        "empresas": Empresa.objects.count(),
        "clientes": Cliente.objects.count(),
        "ativos": Cliente.objects.filter(status__in=["ativo", "vip", "recorrente", "reativado"]).count(),
        "inativos": Cliente.objects.filter(status__in=["inativo", "perdido"]).count(),
        "risco": abertas.filter(prioridade__in=["alto", "critico"]).count(),
        "oportunidades": abertas.count(),
        "receita": abertas.aggregate(total=Sum("valor_potencial"))["total"] or 0,
        "contatos": HistoricoContato.objects.count(),
    }
    charts = {
        "status": list(Cliente.objects.values("status").annotate(total=Count("id")).order_by("-total")),
        "risco": list(abertas.values("risco").annotate(total=Count("id")).order_by("risco")),
        "empresas": list(Empresa.objects.annotate(total=Count("oportunidades")).values("nome_fantasia", "total")[:8]),
        "contatos": list(
            HistoricoContato.objects.annotate(month=TruncMonth("data_contato"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")[:12]
        ),
    }
    return render(request, "dashboards/dashboard.html", {"metrics": metrics, "charts": charts, "title": "Dashboard Executivo"})


@login_required
def relatorios(request):
    abertas = Oportunidade.objects.filter(status=Oportunidade.Status.ABERTA).select_related("cliente", "empresa")
    reports = {
        "Clientes em risco": abertas.filter(prioridade__in=["alto", "critico"]).order_by("-valor_potencial")[:12],
        "Clientes inativos": Cliente.objects.filter(status__in=["inativo", "perdido"]).select_related("empresa").order_by("-valor_total_gasto")[:12],
        "Clientes VIP": Cliente.objects.filter(valor_total_gasto__gte=8000).select_related("empresa").order_by("-valor_total_gasto")[:12],
        "Receita potencial": abertas.order_by("-valor_potencial")[:12],
        "Acoes realizadas": HistoricoContato.objects.select_related("cliente", "cliente__empresa").order_by("-data_contato")[:12],
        "Oportunidades por segmento": abertas.values("empresa__segmento").annotate(total=Count("id"), receita=Sum("valor_potencial")).order_by("-receita"),
    }
    return render(request, "relatorios/index.html", {"reports": reports, "title": "Relatorios"})
