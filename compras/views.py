from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from compras.models import Compra
from collections import Counter


@login_required
def visualizar_compras(request: HttpRequest):
    compras = Compra.objects.all()
    return render(request, 'compras/compras.html', {'compras': compras})

@login_required
def excluir_compra(request: HttpRequest, id):
    Compra.objects.get(id=id).delete()
    return redirect('visualizar_compras')
