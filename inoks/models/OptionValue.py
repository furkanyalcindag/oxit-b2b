from django.db import models

from inoks.models import Option


class OptionValue(models.Model):
    name = models.TextField(null=True, blank=True, verbose_name="Şeçenek Değeri")
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
