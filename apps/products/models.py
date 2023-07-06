from barcodenumber import check_code_ean13
from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    barcode = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def clean(self):
        self.clean_barcode()

    def clean_barcode(self):
        if not check_code_ean13(self.barcode):
            raise ValidationError('Código de barras inválido.')
