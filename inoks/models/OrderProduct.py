from django.db import models

from inoks.models import Order, Product


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    totalProductPrice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=True)
    quantity = models.IntegerField(blank=True, null=True)
