from io import BytesIO

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from apps.compras.models import Compra
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


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
