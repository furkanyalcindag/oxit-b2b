from django.db import models


class PaymentType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    isActive = models.BooleanField()


    def __str__(self):
        return '%d ' % self.name