from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from oportunidades.models import Oportunidade


@login_required
def oportunidade_list(request):
    qs = Oportunidade.objects.select_related("cliente", "empresa")
    for field in ["empresa_id", "prioridade", "status", "tipo"]:
        value = request.GET.get(field)
        if value:
            qs = qs.filter(**{field: value})
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    return render(request, "oportunidades/list.html", {"page_obj": page, "title": "Oportunidades"})


@login_required
def oportunidade_detail(request, pk):
    oportunidade = get_object_or_404(Oportunidade.objects.select_related("cliente", "empresa"), pk=pk)
    return render(request, "oportunidades/detail.html", {"oportunidade": oportunidade, "title": oportunidade.tipo})


@login_required
def oportunidade_status(request, pk, status):
    oportunidade = get_object_or_404(Oportunidade, pk=pk)
    allowed = {choice[0] for choice in Oportunidade.Status.choices}
    if status in allowed:
        oportunidade.status = status
        oportunidade.save(update_fields=["status", "updated_at"])
    return redirect(request.META.get("HTTP_REFERER", "oportunidades_list"))
