from io import BytesIO

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from apps.compras.models import Compra


def get_relatorio_ultima_compra():
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Fetch your products from the database or any other source.
    compra = Compra.objects.latest('id')
    compra_produtos = compra.compra_produtos.all()

    # Set up the table headers.
    table_headers = ['Produto', 'Quantidade', 'Preço Unitário']

    

    # Set up the table rows.
    table_rows = [[compra_produto.produto.nome, str(compra_produto.quantidade), str(compra_produto.preco_unitario)] for compra_produto in compra_produtos]

    # Define the width and height of the table.
    table_width = 100
    table_height = 70

    # Set up the table styles.
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    # Create the table and specify the styles.
    table = Table([table_headers] + table_rows, colWidths=table_width, rowHeights=table_height)
    table.setStyle(TableStyle(style))

    # Draw the table on the PDF.
    table.wrapOn(p, 50, 50)
    table.drawOn(p, 50, 50)

    # Close the PDF object cleanly and return the PDF data.
    p.showPage()
    p.save()

    # File buffer reset.
    buffer.seek(0)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_report.pdf"'

    # Write the PDF data to the response.
    response.write(buffer.getvalue())

    return response