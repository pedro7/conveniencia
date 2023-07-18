from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from apps.colaboradores.models import Colaborador
from apps.compras.models import Compra, CompraProduto

from .referencias import get_referencia_passada, get_referencia_atual


def get_relatorio_ultima_compra():
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Fetch your products from the database or any other source.
    compra = Compra.objects.latest('id')
    compra_produtos = compra.compra_produtos.all()

    # Set up the table headers.
    table_headers = ['Produto', 'Quantidade', 'Preço Unitário']

    # Set up the table rows.
    table_rows = [[compra_produto.produto.nome, str(compra_produto.quantidade), str(compra_produto.preco_unitario)] for compra_produto in compra_produtos]

    # Define the table style.
    style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Header background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Row background color
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Row text color
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text color
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid color
])


    # Create the table and apply the style.
    data = [table_headers] + table_rows
    table = Table(data, repeatRows=1)
    table.setStyle(style)

    # Create the PDF document.
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Build the document content.
    content = []
    content.append(Paragraph('Relatório de Última Compra', getSampleStyleSheet()['Title']))
    content.append(Paragraph('Detalhes da Compra:', getSampleStyleSheet()['Heading2']))
    content.append(table)

    # Build the PDF document.
    doc.build(content)

    # File buffer reset.
    buffer.seek(0)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_report.pdf"'

    # Write the PDF data to the response.
    response.write(buffer.getvalue())

    return response

def get_relatorio_consumo_colaborador(colaborador):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Consumo referência atual e passada.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []

    style = getSampleStyleSheet()

    data_atual = []
    data_passada = []
    table_headers = ['Data', 'Produtos']

    for compra in Compra.objects.filter(colaborador=colaborador, data__gte=get_referencia_atual()):
        row = [
            datetime.strptime(str(compra.data), "%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y %H:%M:%S"),
            ''
        ]
        compra_produtos = CompraProduto.objects.filter(compra=compra)
        produtos_table = create_produtos_table(compra_produtos)
        row[1] = produtos_table
        data_atual.append(row)

    for compra in Compra.objects.filter(colaborador=colaborador, data__range=[get_referencia_passada(), get_referencia_atual()]):
        row = [
            datetime.strptime(str(compra.data), "%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y %H:%M:%S"),
            ''
        ]
        compra_produtos = CompraProduto.objects.filter(compra=compra)
        produtos_table = create_produtos_table(compra_produtos)
        row[1] = produtos_table
        data_passada.append(row)

    story.append(Paragraph('<b>Referência Atual</b>', style['Heading2']))
    table_data_atual = [table_headers] + data_atual
    table_atual = Table(table_data_atual, repeatRows=1)
    table_atual.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(table_atual)
    story.append(Paragraph('<br/><br/>', style['Normal']))

    story.append(Paragraph('<b>Referência Passada</b>', style['Heading2']))
    table_data_passada = [table_headers] + data_passada
    table_passada = Table(table_data_passada, repeatRows=1)
    table_passada.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(table_passada)

    doc.build(story)

    return response


def create_produtos_table(compra_produtos):
    table_data = [['Produto', 'Quantidade', 'Preço Unitário']]
    for compra_produto in compra_produtos:
        row = [
            compra_produto.produto.nome,
            compra_produto.quantidade,
            f'R$ {compra_produto.preco_unitario}'
        ]
        table_data.append(row)

    produtos_table = Table(table_data)
    produtos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    return produtos_table


def get_relatorio_consumo_geral(request):
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

def get_relatorio_total_mensal(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Total_Mensal.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []

    style = getSampleStyleSheet()

    # Title
    story.append(Paragraph('<b>Total Mensal</b>', style['Title']))

    # Total Gasto
    total_gasto = 0
    for compra in Compra.objects.filter(data__month=timezone.now().month):
        for compra_produto in CompraProduto.objects.filter(compra=compra):
            total_gasto += compra_produto.preco_unitario * compra_produto.quantidade

    story.append(Paragraph(f'<b>Total Gasto:</b> R${total_gasto}', style['Normal']))

    doc.build(story)

    return response

def get_relatorio_mudanca_preco_produto(produto, preco_novo, preco_antigo):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Alteração de preço.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []

    style = getSampleStyleSheet()

    
    story.append(Paragraph(f'<b>Produto:</b> {produto.nome}', style['Heading2']))

    data = []
    table_headers = ['Produto', 'Preço Antigo', 'Preço Novo']

    row = [
        produto.nome,
        f'R$ {preco_antigo}',
        f'R$ {preco_novo}'
    ]

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