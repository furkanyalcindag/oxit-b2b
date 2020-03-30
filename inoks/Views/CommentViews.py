from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from inoks.models import Product, Profile, Rating


def Comment(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    product = Product.objects.get(pk=pk)
    ratings = Rating.objects.all()
    rating = Rating.objects.filter(profile=profile).filter(product=product)
    if rating.count() <= 0:
        if request.method == 'POST':
            rating = Rating()
            comment = request.POST['text']
            point = request.POST['star']
            rating.product = product
            rating.profile = profile
            rating.point = point
            rating.comment = comment
            rating.save()
            messages.success(request, 'Yorum Yapıldı')
    else:

        messages.warning(request, "Ürüne daha önceden yorum yaptınız.")
        return redirect('inoks:urun-detay', product.slug)
    return render(request, 'kullanici/kullanici-siparis-urunleri.html', {'ratings': ratings})
