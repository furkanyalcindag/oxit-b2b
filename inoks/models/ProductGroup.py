from django.db import models

from inoks.models.Product import Product


class ProductGroup(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    products = models.ManyToManyField(Product)
