from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from clientes.models import Cliente
from oportunidades.models import Oportunidade
from relacionamento.forms import HistoricoContatoForm
from relacionamento.models import HistoricoContato


@login_required
def fila_carine(request):
    oportunidades = (
        Oportunidade.objects.filter(status__in=[Oportunidade.Status.ABERTA, Oportunidade.Status.EM_ANDAMENTO])
        .select_related("cliente", "empresa")
        .order_by("prioridade", "-valor_potencial")
    )
    grupos = {
        "critico": oportunidades.filter(prioridade="critico"),
        "alto": oportunidades.filter(prioridade="alto"),
        "medio": oportunidades.filter(prioridade="medio"),
        "baixo": oportunidades.filter(prioridade="baixo"),
    }
    return render(request, "relacionamento/fila.html", {"grupos": grupos, "title": "Fila da Carine"})


@login_required
def marcar_contatado(request, pk):
    oportunidade = get_object_or_404(Oportunidade.objects.select_related("cliente"), pk=pk)
    now = timezone.now()
    HistoricoContato.objects.create(
        cliente=oportunidade.cliente,
        oportunidade=oportunidade,
        usuario=request.user,
        data_contato=now,
        tipo_contato="WhatsApp",
        resultado="Contato realizado",
        observacao="Acao registrada pela Fila da Carine.",
        proxima_acao="Acompanhar retorno",
        data_proxima_acao=(now + timedelta(days=15)).date(),
    )
    oportunidade.status = Oportunidade.Status.EM_ANDAMENTO
    oportunidade.save(update_fields=["status", "atualizado_em"])
    oportunidade.cliente.ultimo_atendimento = now.date()
    oportunidade.cliente.status = Cliente.Status.REATIVADO
    oportunidade.cliente.save(update_fields=["ultimo_atendimento", "status", "atualizado_em"])
    return redirect("fila_carine")


@login_required
def reagendar(request, pk):
    oportunidade = get_object_or_404(Oportunidade, pk=pk)
    oportunidade.data_reagendamento = (timezone.now() + timedelta(days=7)).date()
    oportunidade.save(update_fields=["data_reagendamento", "atualizado_em"])
    return redirect("fila_carine")


@login_required
def historico(request):
    qs = HistoricoContato.objects.select_related("cliente", "cliente__empresa", "usuario")
    cliente_id = request.GET.get("cliente")
    if cliente_id:
        qs = qs.filter(cliente_id=cliente_id)
    return render(request, "relacionamento/historico.html", {"historicos": qs[:100], "title": "Historico de Contatos"})


@login_required
def contato_form(request):
    form = HistoricoContatoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        contato = form.save(commit=False)
        contato.usuario = request.user
        contato.save()
        contato.cliente.ultimo_atendimento = contato.data_contato.date()
        contato.cliente.save(update_fields=["ultimo_atendimento", "atualizado_em"])
        return redirect("historico_contatos")
    return render(request, "relacionamento/form.html", {"form": form, "title": "Novo contato"})
