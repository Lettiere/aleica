from datetime import date
from decimal import Decimal

from django.db import transaction

from clientes.models import Cliente
from inteligencia.models import SnapshotInteligencia
from oportunidades.models import Oportunidade


def calcular_dias_sem_retorno(cliente):
    if not cliente.ultimo_atendimento:
        return 999
    return max(0, (date.today() - cliente.ultimo_atendimento).days)


def calcular_risco(cliente):
    days = calcular_dias_sem_retorno(cliente)
    if days <= 90:
        return "baixo"
    if days <= 180:
        return "medio"
    if days <= 365:
        return "alto"
    return "critico"


def calcular_score_aleica(cliente):
    days = calcular_dias_sem_retorno(cliente)
    spent = Decimal(cliente.valor_total_gasto or 0)
    buys = int(cliente.quantidade_compras or 0)
    recency = max(0, 42 - int(days // 8))
    value = min(24, int(spent // Decimal("450")))
    frequency = min(22, buys * 3)
    relationship = 12 if buys >= 6 else 8 if buys >= 3 else 3
    penalty = 18 if days > 365 else 10 if days > 180 else 5 if days > 90 else 0
    return max(0, min(100, recency + value + frequency + relationship - penalty))


def calcular_probabilidade_perda(cliente):
    days = calcular_dias_sem_retorno(cliente)
    spent = Decimal(cliente.valor_total_gasto or 0)
    buys = max(1, int(cliente.quantidade_compras or 1))
    status = str(cliente.status or "").lower()
    base = min(76, int(days // Decimal("5.5")))
    frequency_protection = min(28, buys * 3)
    vip_risk = 15 if spent >= Decimal("8000") and days > 150 else 0
    abandoned_quote = 12 if "orcamento" in status or "orçamento" in status else 0
    inactive = 9 if "inativo" in status else 0
    return max(4, min(97, base - frequency_protection + vip_risk + abandoned_quote + inactive + 20))


def calcular_valor_potencial(cliente):
    spent = Decimal(cliente.valor_total_gasto or 0)
    buys = max(1, int(cliente.quantidade_compras or 1))
    ticket = max(Decimal("250"), spent / buys)
    probability = Decimal(calcular_probabilidade_perda(cliente)) / Decimal("100")
    return max(Decimal("350"), ticket * (Decimal("1") + probability)).quantize(Decimal("0.01"))


def gerar_motivo_alerta(cliente):
    days = calcular_dias_sem_retorno(cliente)
    spent = Decimal(cliente.valor_total_gasto or 0)
    status = str(cliente.status or "").lower()
    if "orcamento" in status or "orçamento" in status:
        return f"Orcamento pendente ha {days} dias."
    if spent >= Decimal("8000") and days >= 150:
        return f"Cliente VIP sem contato ha {days} dias."
    if days > 365:
        return f"Cliente sem retorno ha {days} dias."
    if days > 180:
        return f"Cliente sem acompanhamento ha {days} dias."
    if cliente.quantidade_compras >= 3 and days > 90:
        return f"Cliente recorrente sem pos-venda ha {days} dias."
    if cliente.quantidade_compras <= 1 and days > 60:
        return f"Cliente sem recompra ha {days} dias."
    return "Cliente com relacionamento dentro do ciclo esperado."


def gerar_acao_sugerida(cliente):
    days = calcular_dias_sem_retorno(cliente)
    spent = Decimal(cliente.valor_total_gasto or 0)
    status = str(cliente.status or "").lower()
    if "orcamento" in status or "orçamento" in status:
        return "Retomar proposta com prazo, contexto e beneficio claro."
    if spent >= Decimal("8000") and days >= 150:
        return "Contato consultivo feito pela Carine para reaproximacao."
    if days > 365:
        return "Campanha humana de reativacao e escuta de necessidade atual."
    if days > 180:
        return "Contato de relacionamento para recuperar vinculo comercial."
    if cliente.quantidade_compras >= 3 and days > 90:
        return "Realizar pos-venda e mapear proxima oportunidade."
    if cliente.quantidade_compras <= 1 and days > 60:
        return "Apresentar complemento natural a primeira compra."
    return "Manter acompanhamento planejado."


def classificar_oportunidade(cliente):
    days = calcular_dias_sem_retorno(cliente)
    spent = Decimal(cliente.valor_total_gasto or 0)
    status = str(cliente.status or "").lower()
    if "orcamento" in status or "orçamento" in status:
        return "Orcamento abandonado", "alto" if days > 60 else "medio"
    if spent >= Decimal("8000") and days >= 150:
        return "Cliente VIP sem retorno", "critico" if days > 240 else "alto"
    if days > 365:
        return "Cliente inativo", "critico"
    if days > 180:
        return "Cliente em risco", "alto"
    if cliente.quantidade_compras >= 3 and days > 90:
        return "Pos-venda pendente", "medio"
    if cliente.quantidade_compras <= 1 and days > 60:
        return "Oportunidade de reativacao", "medio"
    return "Relacionamento saudavel", calcular_risco(cliente)


@transaction.atomic
def gerar_oportunidades(cliente):
    tipo, prioridade = classificar_oportunidade(cliente)
    if tipo == "Relacionamento saudavel":
        Oportunidade.objects.filter(cliente=cliente, status=Oportunidade.Status.ABERTA).update(status=Oportunidade.Status.CONCLUIDA)
        return None
    oportunidade, _ = Oportunidade.objects.update_or_create(
        cliente=cliente,
        status=Oportunidade.Status.ABERTA,
        defaults={
            "empresa": cliente.empresa,
            "tipo": tipo,
            "prioridade": prioridade,
            "score": calcular_score_aleica(cliente),
            "probabilidade_perda": calcular_probabilidade_perda(cliente),
            "valor_potencial": calcular_valor_potencial(cliente),
            "motivo": gerar_motivo_alerta(cliente),
            "descricao": f"Oportunidade identificada pela inteligencia Aleica para {cliente.nome}.",
            "acao_sugerida": gerar_acao_sugerida(cliente),
            "risco": calcular_risco(cliente),
        },
    )
    return oportunidade


def atualizar_inteligencia_empresa(empresa):
    snapshots = []
    for cliente in Cliente.objects.filter(empresa=empresa):
        snapshots.append(
            SnapshotInteligencia.objects.create(
                empresa=cliente.empresa,
                cliente=cliente,
                score_aleica=calcular_score_aleica(cliente),
                risco=calcular_risco(cliente),
                probabilidade_perda=calcular_probabilidade_perda(cliente),
                dias_sem_retorno=calcular_dias_sem_retorno(cliente),
                valor_potencial=calcular_valor_potencial(cliente),
                motivo_alerta=gerar_motivo_alerta(cliente),
            )
        )
        gerar_oportunidades(cliente)
    return snapshots
