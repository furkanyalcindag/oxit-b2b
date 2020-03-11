from django.contrib.auth.models import User
from django.db import models

from inoks.models import City, Job
from inoks.models.CreditCard import CreditCard
from inoks.models.Enum import GENDER_CHOICES, MALE, SCHOOL_CHOICES, ilkokul


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profil Resmi')
    tc = models.CharField(max_length=11, null=True, blank=True, verbose_name='T.C. Kimlik Numarası')
    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    mobilePhone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Telefon Numarası')
    # address = models.TextField(blank=True, null=True, verbose_name='Adres')
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    gender = models.CharField(max_length=128, null=True, blank=True, verbose_name='Cinsiyeti', choices=GENDER_CHOICES,
                              default=MALE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='İl')
    district = models.TextField(blank=True, null=True, verbose_name='İlçe')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Meslek')
    educationLevel = models.CharField(max_length=128, null=True, blank=True, verbose_name="Eğitim Düzeyi",
                                      choices=SCHOOL_CHOICES,
                                      default=ilkokul)

    isApprove = models.BooleanField(default=False, null=True, blank=True)
    isActive = models.BooleanField(default=False)
    isContract = models.BooleanField(default=False)
    isNotification = models.BooleanField(default=False,null=True,blank=True)
    activePassiveDate = models.DateTimeField(null=True, blank=True)
    # creditCard = models.ManyToManyField(CreditCard, null=True, blank=True, verbose_name='Kredi Kartı')
    iban = models.TextField(blank=True, null=True, verbose_name='iban')
    ibanAdSoyad = models.TextField(blank=True, null=True, verbose_name='ibanAdSoyad')

    def __str__(self):
        return '%d %s %s %s' % (self.id, '-', self.user.first_name, self.user.last_name)
