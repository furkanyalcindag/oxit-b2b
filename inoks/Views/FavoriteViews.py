from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from inoks.models import FavoriteProduct, Profile, Product
from inoks.services import general_methods


@login_required
def Favorites(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    favorites = FavoriteProduct.objects.filter(profile=profile)

    return render(request, 'favoriler/favori-urunler.html', {'products': favorites})


@api_view(http_method_names=['POST'])
def add_favorite_product(request):
    if request.POST:
        try:

            product = Product.objects.get(pk=request.POST.get('product'))
            user = request.user
            profile = Profile.objects.get(user=user)
            favorite = FavoriteProduct.objects.filter(product=product)
            if favorite.count() == 0:
                favorite_product = FavoriteProduct()
                favorite_product.profile = profile
                favorite_product.product = product
                favorite_product.product_price = product.price
                favorite_product.save()

                return JsonResponse({'status': 'Success', 'msg': "Favori ürün eklendi", 'message_type': 'success','code':100})
            else:
                return JsonResponse({'status': 'Success', 'msg': "Ürün Favorilerimde mevcut", 'message_type': 'success','code':101})
        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def delete_favorite_product(request, pk):
    obj = FavoriteProduct.objects.get(product=pk)
    obj.delete()
    messages.success(request, 'Ürün Favorilerimden Kaldırıldı.')

    return redirect('inoks:favori-urunler')
