from django.db import models

from inoks.models.PaymentMethod import PaymentMethod


class PaymentMethodBakiyem(models.Model):
    payment_type = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='Kullanıcı Adı')
    password = models.CharField(max_length=100, null=True, blank=True, verbose_name="Şifre")
    dealerCode = models.CharField(max_length=100, null=True, blank=True, verbose_name="DealerCode")

    def __str__(self):
        return '%s ' % self.username
