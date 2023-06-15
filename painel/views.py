from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def painel(request: HttpRequest):
    if request.user.is_superuser:
        return render(request, 'painel-admin.html')
    else:
        return render(request, 'painel.html')
