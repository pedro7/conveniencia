from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def painel(request: HttpRequest):
    return render(request, 'painel/painel.html')
