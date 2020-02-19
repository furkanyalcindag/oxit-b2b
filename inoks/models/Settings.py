from django.db import models
from django.contrib.auth.models import auth, Permission


class Settings(models.Model):
    name = models.CharField(max_length=120, null=True)
    value = models.TextField(blank=True, null=True)

