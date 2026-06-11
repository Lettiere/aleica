from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import render

from clientes.models import Cliente
from inteligencia.services import calcular_probabilidade_perda, calcular_risco, calcular_score_aleica, calcular_valor_potencial
from oportunidades.models import Oportunidade


@login_required
def inteligencia(request):
    clientes = list(Cliente.objects.select_related("empresa"))
    enriched = [
        {
            "cliente": cliente,
            "score": calcular_score_aleica(cliente),
            "risco": calcular_risco(cliente),
            "probabilidade": calcular_probabilidade_perda(cliente),
            "valor": calcular_valor_potencial(cliente),
        }
        for cliente in clientes
    ]
    enriched.sort(key=lambda item: (item["risco"] != "critico", -item["probabilidade"], -item["valor"]))
    abertas = Oportunidade.objects.filter(status=Oportunidade.Status.ABERTA)
    context = {
        "title": "Inteligencia Comercial",
        "maior_risco": enriched[:12],
        "vips": [item for item in enriched if item["cliente"].valor_total_gasto >= 8000][:12],
        "inativos": [item for item in enriched if item["risco"] in ["alto", "critico"]][:12],
        "reativacao": list(abertas.order_by("-probabilidade_perda")[:12]),
        "score_medio": round(sum(item["score"] for item in enriched) / len(enriched), 1) if enriched else 0,
        "receita_potencial": abertas.aggregate(total=Sum("valor_potencial"))["total"] or 0,
    }
    return render(request, "inteligencia/index.html", context)
