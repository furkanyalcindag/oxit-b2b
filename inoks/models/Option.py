from django.db import models

from inoks.models.Enum import OPTION_CHOICES, OPTION1


class Option(models.Model):
    type_name = models.CharField(max_length=256, null=True, blank=True, verbose_name="Şeçenek Adı")
    type = models.TextField(choices=OPTION_CHOICES, default=OPTION1, verbose_name="Seçenek Tipi", null=True, blank=True)

