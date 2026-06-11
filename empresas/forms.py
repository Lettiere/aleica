from django import forms

from empresas.models import Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ["nome_fantasia", "razao_social", "cnpj", "segmento", "telefone", "email", "cidade", "estado", "status"]
        widgets = {field: forms.TextInput(attrs={"class": "form-control"}) for field in fields}
        widgets["status"] = forms.Select(attrs={"class": "form-select"})
