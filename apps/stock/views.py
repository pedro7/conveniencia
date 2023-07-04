from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from .models import Stock


@login_required
def visualizar_estoque(request: HttpRequest):
    stocks = Stock.objects.all()
    return render(request, 'stock/stock.html', {'stocks': stocks})
