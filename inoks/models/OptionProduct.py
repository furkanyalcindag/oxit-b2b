from django.db import models

from inoks.models import Product
from inoks.models.OptionValue import OptionValue


class OptionProduct(models.Model):
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    list_price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True, verbose_name='Stok Adedi')
