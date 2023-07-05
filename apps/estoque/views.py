from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from .models import Estoque


@login_required
def visualizar_estoque(request: HttpRequest):
    estoques = Estoque.objects.all()
    return render(request, 'estoque/estoque.html', {'estoques': estoques})
