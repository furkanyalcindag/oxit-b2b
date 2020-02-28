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
    c_code = ""
    subtotal = 0
    discount = 0
    net_total = 0
    total = 0
    kargo = Cargo.objects.get(name='Üzeri Kargo')
    kargo1 = 0
    kdv = Settings.objects.get(name='kdv')

    user = request.user
    user_form = UserUpdateForm(request.POST or None, instance=user)
    profile = Profile.objects.get(user=user)
    profile_form = LoginProfilForm(request.POST or None, instance=profile)

    addresses = AddressProfile.objects.filter(profile=profile)
    address_dict = dict()
    orders = []



    if request.POST:

        if user_form.is_valid() and profile_form.is_valid():

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            profile.mobilePhone = profile_form.cleaned_data['mobilePhone']

            user.save()
            profile_form.save()

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
        c_code = json.loads(request.POST['c_code'])
        code = c_code['c_code']

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

        discount = couponControl(code, subtotal)

        if orders:
            net_total = subtotal * 100 / (100 + float(kdv.value))
            if subtotal >= kargo.lower_limit:  # KARGO KONTROLU
                kargo1 = 0
                total = subtotal - float(discount)
                kdv = Decimal(total) - Decimal(net_total)

            else:
                kargo1 = kargo.price
                total = Decimal(subtotal) + kargo.price - float(discount)
                kdv = Decimal(total) - Decimal(net_total)

    return render(request, 'checkout/odeme-tamamla-login.html',
                  {'card': orders, 'user_form': user_form, 'profile_form': profile_form, 'subtotal': Decimal(subtotal),
                   'total': Decimal(total),
                   'net_total': Decimal(net_total),
                   'kdv': Decimal(kdv), 'kargo1': kargo1, 'addresses': address_dict, 'discount': discount})


@login_required
def add_payment_address(request):
    current_user = request.user
    perm = general_methods.control_access(request)

    if not perm and request.user == current_user:
        logout(request)
        return redirect('accounts:login')

    address_form = AddressForm(request.POST)

    profile = Profile.objects.get(user=current_user)

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():

            userAddress = Address(name=address_form.cleaned_data['name'],
                                  address=address_form.cleaned_data['address'],
                                  city=address_form.cleaned_data['city'],
                                  district=address_form.cleaned_data['district'])
            userAddress.save()
            address_profile = AddressProfile(profile=profile, address=userAddress)
            address_profile.save()
            messages.success(request, 'Adres Eklendi')
            return redirect('inoks:odeme-tamamla-user')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'checkout/odeme-tamamla-login.html',
                  {'address_form': address_form})
