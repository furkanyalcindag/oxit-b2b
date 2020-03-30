from django.db import models

from inoks.models import Profile, Product


class Rating(models.Model):
    comment = models.TextField(verbose_name="Yorum", null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Yorum Yapılma Tarihi')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="yorum yapılan ürün")
    point = models.IntegerField(null=True, blank=True, verbose_name="Puan")
