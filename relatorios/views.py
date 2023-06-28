from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from reportlab.pdfgen.canvas import Canvas

from colaboradores.models import Colaborador
from compras.models import Compra, CompraProduto


@login_required
def visualizar_relatorios(request: HttpRequest):
    if not request.user.is_superuser:
        return redirect('entrar')
    return render(request, 'relatorios/relatorios.html')

# limpar
@login_required
def gerar_total_mensal(request: HttpRequest):
    if not request.user.is_superuser:
        return redirect('entrar')
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename="Total_Mensal.pdf"'
    p = Canvas(response)
    p.setFont("Helvetica", 12)  # Set the font and size
    p.drawString(50, 750, "Total mensal:")  # Write the text at the specified coordinates
    mes_atual = timezone.now().month
    total_gasto = 0
    for compra in Compra.objects.filter(data__month=mes_atual):
        for compra_produto in CompraProduto.objects.filter(compra=compra):
            total_gasto += compra_produto.preco_unitario * compra_produto.quantidade
    p.drawString(50, 725, str(total_gasto))
    p.showPage()
    p.save()
    return response

# limpar
@login_required
def gerar_consumo_geral(request: HttpRequest):
    if not request.user.is_superuser:
        return redirect('entrar')
    data1 = datetime.fromisoformat(request.GET['data']).strftime("%Y-%m-%d %H:%M:%S.%f")
    data2 = datetime.fromisoformat(request.GET['dataa']).strftime("%Y-%m-%d %H:%M:%S.%f")
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename="Consumo_Geral.pdf"'
    p = Canvas(response)
    p.setFont("Helvetica", 12)  # Set the font and size
    y = 750
    for colaborador in Colaborador.objects.all():
        p.drawString(50, y, f'Colaborador: {colaborador.nome}')
        y -= 25
        if y <= 100:
            p.showPage()
            y = 750
        for compra in Compra.objects.filter(colaborador=colaborador, data__range=(data1, data2)):
            p.drawString(75, y, f'Compra id: {compra.id}')
            y -= 25
            if y <= 100:
                p.showPage()
                y = 750
            data = datetime.strptime(str(compra.data), "%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y %H:%M:%S")
            p.drawString(75, y, f'Data: {data}')
            y -= 25
            if y <= 100:
                p.showPage()
                y = 750
            p.drawString(75, y, 'Produtos:')
            y -= 25
            if y <= 100:
                p.showPage()
                y = 750
            compra_produtos = CompraProduto.objects.filter(compra=compra)
            for compra_produto in compra_produtos:
                p.drawString(100, y, f'{compra_produto.produto.nome}   x{compra_produto.quantidade}   R${compra_produto.preco_unitario * compra_produto.quantidade}')
                y -= 25
                if y <= 100:
                    p.showPage()
                    y = 750
    p.save()
    return response 
