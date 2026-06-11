from django import forms
from django.utils import timezone

from relacionamento.models import HistoricoContato


class HistoricoContatoForm(forms.ModelForm):
    class Meta:
        model = HistoricoContato
        fields = ["cliente", "data_contato", "tipo_contato", "resultado", "observacao", "proxima_acao", "data_proxima_acao"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "data_contato": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "tipo_contato": forms.TextInput(attrs={"class": "form-control"}),
            "resultado": forms.TextInput(attrs={"class": "form-control"}),
            "observacao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "proxima_acao": forms.TextInput(attrs={"class": "form-control"}),
            "data_proxima_acao": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get("data_contato"):
            self.initial["data_contato"] = timezone.localtime().strftime("%Y-%m-%dT%H:%M")
