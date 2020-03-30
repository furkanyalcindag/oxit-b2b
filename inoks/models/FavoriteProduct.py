from django.db import models

from inoks.models import Profile, Product


class FavoriteProduct(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True, verbose_name="Favori Liste Adı ")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Favori Ekleme Tarihi')
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
