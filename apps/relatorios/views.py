from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from reportlab.pdfgen.canvas import Canvas

from apps.colaboradores.models import Colaborador
from apps.compras.models import Compra, CompraProduto


@login_required
def visualizar_relatorios(request: HttpRequest):
    if not request.user.is_superuser:
        return redirect('entrar')
    return render(request, 'relatorios/relatorios.html')

# @login_required
# def gerar_total_mensal(request: HttpRequest):
#     if not request.user.is_superuser:
#         return redirect('entrar')
#     response = HttpResponse()
#     response['Content-Disposition'] = 'attachment; filename="Total_Mensal.pdf"'
#     p = Canvas(response)
#     p.setFont("Helvetica", 12)
#     p.drawString(50, 750, "Total mensal:")
#     mes_atual = timezone.now().month
#     total_gasto = 0
#     for compra in Compra.objects.filter(data__month=mes_atual):
#         for compra_produto in CompraProduto.objects.filter(compra=compra):
#             total_gasto += compra_produto.preco_unitario * compra_produto.quantidade
#     p.drawString(50, 725, str(total_gasto))
#     p.showPage()
#     p.save()
#     return response

@login_required
def gerar_total_mensal(request):
    if not request.user.is_superuser:
        return redirect('entrar')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Total_Mensal.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []

    style = getSampleStyleSheet()

    # Title
    story.append(Paragraph('<b>Total Mensal</b>', style['Title']))

    # Month and Year
    current_month = timezone.now().strftime("%B, %Y")
    story.append(Paragraph(f'<b>Mês:</b> {current_month}', style['Normal']))

    # Total Gasto
    total_gasto = 0
    for compra in Compra.objects.filter(data__month=timezone.now().month):
        for compra_produto in CompraProduto.objects.filter(compra=compra):
            total_gasto += compra_produto.preco_unitario * compra_produto.quantidade

    story.append(Paragraph(f'<b>Total Gasto:</b> R${total_gasto}', style['Normal']))

    doc.build(story)

    return response

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from django.http import HttpResponse

def gerar_consumo_geral(request):
    if not request.user.is_superuser:
        return redirect('entrar')

    data1 = datetime.fromisoformat(request.GET['data']).strftime("%Y-%m-%d %H:%M:%S.%f")
    data2 = datetime.fromisoformat(request.GET['dataa']).strftime("%Y-%m-%d %H:%M:%S.%f")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Consumo_Geral.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []

    style = getSampleStyleSheet()

    for colaborador in Colaborador.objects.all():
        story.append(Paragraph(f'<b>Colaborador:</b> {colaborador.nome}', style['Heading2']))

        data = []
        table_headers = ['Compra ID', 'Data', 'Produtos']

        for compra in Compra.objects.filter(colaborador=colaborador, data__range=(data1, data2)):
            row = [
                str(compra.id),
                datetime.strptime(str(compra.data), "%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y %H:%M:%S"),
                ''
            ]
            compra_produtos = CompraProduto.objects.filter(compra=compra)
            produtos = []
            for compra_produto in compra_produtos:
                produtos.append(f'{compra_produto.produto.nome} x{compra_produto.quantidade} R${compra_produto.preco_unitario * compra_produto.quantidade}')

            row[2] = Paragraph('<br/>'.join(produtos), style['Normal'])
            data.append(row)

        table_data = [table_headers] + data
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        story.append(table)
        story.append(Paragraph('<br/><br/>', style['Normal']))

    doc.build(story)

    return response