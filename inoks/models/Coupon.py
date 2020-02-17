from django.db import models

class Coupon(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Kupon Adı')
    code = models.TextField(blank=True, null=True, verbose_name='Kupon Kodu')
    isActive = models.BooleanField(default=False)
    creationDate = models.DateTimeField(verbose_name='Kupon Başlangıç Tarihi')
    finishDate = models.DateTimeField(verbose_name='Kupon Bitiş Tarihi')
    discountAmount = models.IntegerField(blank=True, null=True, verbose_name='İndirim Miktari')



