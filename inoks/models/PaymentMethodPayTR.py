from django.db import models

from inoks.models.PaymentMethod import PaymentMethod


class PaymentMethodPayTR(models.Model):
    payment_type = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    merchantId = models.CharField(max_length=20,blank=True, null=True, verbose_name='MerchantId')
    merchantKey = models.CharField(max_length=100, null=True, blank=True, verbose_name="MerchantKey")
    merchantSalt = models.CharField(max_length=100, null=True, blank=True, verbose_name="MerchantSalt")

    def __str__(self):
        return '%s ' % self.merchantId
