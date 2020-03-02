import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response

from inoks.Forms.AddressForm import AddressForm
from inoks.Forms.GuestUserForm import GuestUserForm
from inoks.Forms.LoginProfilForm import LoginProfilForm
from inoks.Forms.OrderUpdateForm import OrderForm
from inoks.Forms.UserCheckoutForm import UserCheckoutForm
from inoks.Forms.UserUpdateForm import UserUpdateForm
from inoks.models import Product, Profile, Settings, City, Order, OrderProduct, OrderSituations
from inoks.models.Address import Address
from inoks.models.AddressObject import AddressObject
from inoks.models.AddressProfile import AddressProfile
from inoks.models.Cargo import Cargo
from inoks.models.Enum import ADDRESS_CHOISES
from inoks.models.UserProductObject import UserProductObject
from inoks.models.discountObject import discountObject
from inoks.services import general_methods
from inoks.services.general_methods import couponControl
from rest_framework.decorators import api_view


def order_checkout(request):
    orders = []
    subtotal = 0

    net_total = 0
    total = 0
    kargo = Cargo.objects.get(name='Üzeri Kargo')
    kargo1 = 0
    kdv = Settings.objects.get(name='kdv')
    if request.method == 'POST':
        products = json.loads(request.POST['products_cart'])

        for product in products:
            obj = Product.objects.get(id=product['id'])
            order = UserProductObject(id=0, product_name=None, price=0, count=0, image=None, subtotal=0, slug=None)
            order.id = product['id']
            order.slug = obj.slug
            order.product_name = product['name']
            order.price = product['price']
            order.count = product['count']
            order.image = obj.productImage
            order.subtotal = product['count'] * product['price']

            orders.append(order)

        for order in orders:
            subtotal = order.subtotal + subtotal

        if orders:
            net_total = subtotal * 100 / (100 + float(kdv.value))
            if subtotal >= kargo.lower_limit:
                kargo1 = 0
                total = subtotal
                kdv = Decimal(total) - Decimal(net_total)

            else:
                kargo1 = kargo.price
                total = Decimal(subtotal) + kargo.price
                kdv = Decimal(total) - Decimal(net_total)
        return render(request, 'checkout/siparis-detay.html',
                      {'orders': orders, 'subtotal': Decimal(subtotal), 'total': Decimal(total),
                       'net_total': Decimal(net_total),
                       'kdv': Decimal(kdv),
                       'kargo': kargo, 'kargo1': kargo1})

    return render(request, 'checkout/siparis-detay.html',
                  {'orders': orders, 'subtotal': Decimal(subtotal), 'total': Decimal(total),
                   'net_total': Decimal(net_total),
                   'kdv': Decimal(kdv)})


@login_required
def payment_islogin(request):
    card = ""

    subtotal = 0
    discount = 0
    net_total = 0
    total = 0
    kargo = Cargo.objects.get(name='Üzeri Kargo')
    kargo1 = 0
    kdv = Settings.objects.get(name='kdv')
    city = City.objects.all()
    address_title = ADDRESS_CHOISES
    user = request.user
    user_form = UserCheckoutForm(instance=user)
    profile = Profile.objects.get(user=user)
    profile_form = LoginProfilForm(instance=profile)

    addresses = AddressProfile.objects.filter(profile=profile)
    address_dict = dict()
    orders = []

    if request.POST:

        if user_form.is_valid() and profile_form.is_valid():
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            profile.mobilePhone = profile_form.cleaned_data['mobilePhone']

        # user.save()
        # profile_form.save()

        for choice in ADDRESS_CHOISES:
            address_array = []
            for address in addresses.filter(address__name=choice[0]):
                addressobj = AddressObject(id=0, name=None, city=None, district=None, address=None)
                addressobj.id = address.address.pk
                addressobj.name = address.address.name
                addressobj.address = address.address.address
                addressobj.city = address.address.city
                addressobj.district = address.address.district
                address_array.append(addressobj)
            if len(address_array) > 0:
                address_dict[choice[0]] = address_array

        cards = json.loads(request.POST['card'])

        for product in cards:
            order = UserProductObject(id=0, product_name=None, price=0, count=0, image=None, subtotal=0, slug=None)
            order.id = product['id']
            order.product_name = product['name']
            order.price = product['price']
            order.count = product['count']
            order.subtotal = product['count'] * product['price']

            orders.append(order)

        for order in orders:
            subtotal = order.subtotal + subtotal
        c_code = json.loads(request.POST['c_code'])

        if c_code == None:
            discount = discount

        else:
            code = c_code['c_code']
            discount = couponControl(code, subtotal)

        if orders:
            net_total = subtotal * 100 / (100 + float(kdv.value))
            if subtotal >= kargo.lower_limit:  # ücretsiz kargo
                kargo1 = 0
                total = subtotal
                kdv = Decimal(total) - Decimal(net_total)
                total = subtotal - float(discount)

            else:
                kargo1 = kargo.price  # ücretli kargo
                total = Decimal(subtotal)
                kdv = Decimal(total) - Decimal(net_total)
                total = Decimal(subtotal) + kargo.price - float(discount)

    return render(request, 'checkout/odeme-tamamla-login.html',
                  {'card': orders, 'user_form': user_form, 'profile_form': profile_form, 'subtotal': Decimal(subtotal),
                   'total': Decimal(total),
                   'net_total': Decimal(net_total),
                   'kdv': Decimal(kdv), 'kargo1': kargo1, 'addresses': address_dict, 'discount': discount,
                   'city': city, 'adres': address_title})


@api_view(http_method_names=['POST'])
def new_address(request):
    if request.POST:
        discount = 0
        message = ""
        type = ""
        addresses = []
        try:
            address = request.POST.get('address')
            city = request.POST.get('city')
            district = request.POST.get('district')
            address_name = request.POST.get('address_name')

            adres = Address()
            adres.address = address
            adres.city = City.objects.get(pk=int(city))
            adres.district = district
            adres.name = address_name
            il = str(adres.city) + '/' + str(adres.district)
            adres.save()

            profile = Profile.objects.get(user=request.user)

            adresProfile = AddressProfile()
            adresProfile.address = adres
            adresProfile.profile = profile

            adresProfile.save()

            return JsonResponse(
                {'status': 'Success', 'messages': "Adres Başarıyla Eklendi", 'address': adres.address,
                 'il': il,'a_id':adres.pk,
                 'message_type': 'success'
                 })

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': "Adres Eklenemedi", 'message_type': 'error'})
