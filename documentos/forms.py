from django import forms

from documentos.models import Documento


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["empresa", "titulo", "categoria", "arquivo"]
        widgets = {
            "empresa": forms.Select(attrs={"class": "form-select"}),
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contratos, planilhas, fiscal..."}),
            "arquivo": forms.FileInput(attrs={"class": "form-control"}),
        }
