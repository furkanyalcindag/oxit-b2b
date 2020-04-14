from django.contrib import messages

from django.shortcuts import render, redirect

from inoks.models import Product, Profile, Rating


def make_comment(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    product = Product.objects.get(pk=pk)
    ratings = Rating.objects.all()
    point = 0
    rating = Rating.objects.filter(profile=profile).filter(product=product)
    if rating.count() <= 0:
        if request.method == 'POST':
            rating = Rating()
            comment = request.POST['text']
            point = request.POST['point']
            if point == '':
                point = 5
            rating.product = product
            rating.profile = profile
            rating.point = point
            rating.comment = comment
            rating.save()
            messages.success(request, 'Yorum Yapıldı')
            point = int(rating.point) * 20

    else:

        for rating in rating:
            point = rating.point * 20
        messages.warning(request, "Bu Ürünü Daha Önceden Değerlendirdiniz")
        return render(request, 'comment/rating.html',
                      {'rating': rating, 'product': product, 'point': point})
    return render(request, 'comment/rating.html', {'rating': rating, 'product': product, 'point': point})
