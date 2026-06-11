from django import template

from core.utils import money_br, whatsapp_link


register = template.Library()


@register.filter
def money(value):
    return money_br(value)


@register.filter
def badge_class(value):
    return {
        "critico": "text-bg-dark",
        "alto": "text-bg-danger",
        "medio": "text-bg-warning",
        "baixo": "text-bg-success",
        "aberta": "text-bg-primary",
        "em_andamento": "text-bg-info",
        "concluida": "text-bg-success",
        "perdida": "text-bg-secondary",
        "ativo": "text-bg-success",
        "vip": "text-bg-primary",
        "recorrente": "text-bg-info",
        "inativo": "text-bg-warning",
        "perdido": "text-bg-dark",
        "reativado": "text-bg-success",
    }.get(str(value), "text-bg-secondary")


@register.simple_tag
def wa_link(phone, name=""):
    return whatsapp_link(phone, name)
