from django.db import models

from inoks.models import Profile, City
from inoks.models.PaymentType import PaymentType
from inoks.models.Cargo import Cargo
from inoks.models.OrderSituations import OrderSituations
from inoks.models.Product import Product
from inoks.models.Enum import PAYMENT_CHOICES, TRANSFER


class Order(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Üye Adı')
    product = models.ManyToManyField(Product, through='OrderProduct')
    order_situations = models.ManyToManyField(OrderSituations, default='Ödeme Bekliyor')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Sipariş Adeti')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl')
    district = models.TextField(blank=True, null=True, verbose_name='İlçe')
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    sponsor = models.TextField(blank=True, null=True, verbose_name='Sponsor')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, verbose_name='Ödeme Türü', )
    isContract = models.BooleanField(default=False)
    isApprove = models.BooleanField(default=False)
    cargo = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True)
    kdv = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True, verbose_name="KDV")
    discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True, verbose_name="İndirim")
    net_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True)
    subTotal=models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True)
    isPayed = models.BooleanField(default=False)
    totalPrice = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    paidDate = models.DateTimeField(null=True, blank=True, verbose_name='Kayıt Tarihi')
    otherAddress = models.TextField(blank=True, null=True, verbose_name='Diğer Adres')
    companyInfo = models.TextField(blank=True, null=True, verbose_name='Şirket Bilgileri')

    def __str__(self):
        return '%d ' % self.id

    def latest_catch(self):
        if len(self.order_situations.all()) > 0:
            return self.order_situations.all()[len(self.order_situations.all()) - 1]
        else:
            return 0
