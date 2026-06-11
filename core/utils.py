from decimal import Decimal
from urllib.parse import quote


def money_br(value):
    value = Decimal(value or 0)
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def whatsapp_link(phone, name=""):
    digits = "".join(ch for ch in str(phone or "") if ch.isdigit())
    if digits and not digits.startswith("55"):
        digits = f"55{digits}"
    text = quote(f"Ola, {name}! Aqui e a Carine da Aleica. Posso falar com voce?")
    return f"https://wa.me/{digits}?text={text}" if digits else "#"
