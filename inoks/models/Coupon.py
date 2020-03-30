from django.db import models


class Coupon(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Kupon Adı')
    code = models.TextField(blank=True, null=True, verbose_name='Kupon Kodu')
    isActive = models.BooleanField(default=False)
    creationDate = models.DateTimeField(verbose_name='Kupon Başlangıç Tarihi')
    finishDate = models.DateTimeField(verbose_name='Kupon Bitiş Tarihi')
    stock = models.IntegerField(blank=True, null=True, verbose_name='Kupon Adedi')
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    isLimit = models.BooleanField(default=False)
    limit = models.DecimalField(max_digits=8, decimal_places=2, null=True)
