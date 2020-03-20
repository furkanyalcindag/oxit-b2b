from django.db import models

from inoks.models import Order


class IyzicoToken(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    token = models.CharField(max_length=200, null=True, blank=True)
