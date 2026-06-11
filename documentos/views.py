from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from documentos.forms import DocumentoForm
from documentos.models import Documento


@login_required
def documento_list(request):
    q = request.GET.get("q", "")
    qs = Documento.objects.select_related("empresa").filter(ativo=True)
    if q:
        qs = qs.filter(titulo__icontains=q) | qs.filter(categoria__icontains=q) | qs.filter(empresa__nome_fantasia__icontains=q)
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    return render(request, "documentos/list.html", {"page_obj": page, "q": q, "title": "Documentos"})


@login_required
def documento_upload(request):
    form = DocumentoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Documento enviado.")
        return redirect("documentos_list")
    return render(request, "documentos/form.html", {"form": form, "title": "Enviar documento"})


@login_required
def documento_download(request, pk):
    documento = get_object_or_404(Documento, pk=pk, ativo=True)
    return FileResponse(documento.arquivo.open("rb"), as_attachment=True, filename=documento.arquivo.name.split("/")[-1])
