from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def compras(request: HttpRequest):
    return render(request, 'compras.html')
