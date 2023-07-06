from django.db import models

from apps.products.models import Product


class Stock(models.Model):
    product = models.OneToOneField(Product, models.CASCADE)
