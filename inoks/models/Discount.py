from django.db import models

from inoks.models import Product


class Discount(models.Model):
    isDiscountReseller = models.BooleanField(default=False, null=True, blank=True, verbose_name="Bayi için İndirim")
    isDiscountCustomer = models.BooleanField(default=False, null=True, blank=True, verbose_name="Müşteri için İndirim")
    discountPriceReseller = models.DecimalField(null=True, blank=True,max_digits=8, decimal_places=2,
                                                verbose_name="Bayi için İndirimli Fiyat")
    discountPriceCustomer = models.DecimalField(null=True, blank=True,max_digits=8, decimal_places=2,
                                                verbose_name="Müşteri İçin İndirimli Fiyat")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(verbose_name='İndirimin Başlangıç Tarihi')
    finishDate = models.DateTimeField(verbose_name='İndirimin Bitiş Tarihi')
