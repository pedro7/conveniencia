from django.db import models

from apps.collaborators.models import Collaborator
from apps.products.models import Product


class Purchase(models.Model):
    collaborator = models.ForeignKey(Collaborator, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, through='PurchaseProduct')
    date = models.DateTimeField(auto_now_add=True)


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_product')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=4, decimal_places=2)
