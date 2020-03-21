from django.db import models


class Notification(models.Model):

    key = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(verbose_name='Bildirim İçeriği', null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.key, '-', self.message,)
