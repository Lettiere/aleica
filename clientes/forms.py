from django import forms

from clientes.models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "empresa",
            "nome",
            "cnpj",
            "telefone",
            "whatsapp",
            "email",
            "origem",
            "ultimo_atendimento",
            "valor_total_gasto",
            "quantidade_compras",
            "status",
            "observacoes",
        ]
        widgets = {
            "empresa": forms.Select(attrs={"class": "form-select"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cnpj": forms.TextInput(attrs={"class": "form-control", "data-cnpj-field": "true", "placeholder": "00.000.000/0001-00"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "whatsapp": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "origem": forms.TextInput(attrs={"class": "form-control"}),
            "ultimo_atendimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "valor_total_gasto": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "quantidade_compras": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
