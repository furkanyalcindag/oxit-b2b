from django.db import models

from inoks.models import Product, Order, Profile
from inoks.models.RefundSituations import RefundSituations


class Refund(models.Model):
    Evet = 'Evet'
    Hayir = 'Hayır'

    OPEN_CHOICES = (
        (Evet, 'Evet'),
        (Hayir, 'Hayır'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Sipariş Numarası')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Ürün Adı')

    orderQuantity = models.IntegerField(null=True, blank=True, verbose_name='Adet')
    refundSituations = models.ManyToManyField(RefundSituations)
    refundDate = models.DateTimeField(auto_now_add=True, verbose_name='İade Tarihi')
    isOpen = models.CharField(max_length=128, verbose_name='Cinsiyeti', choices=OPEN_CHOICES, default=Hayir)
    isApprove = models.BooleanField(null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%s ' % self.product.name
