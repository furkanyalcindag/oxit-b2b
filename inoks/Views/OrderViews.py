import base64
import binascii
import hashlib
import hmac
import json
import pickle
import sys

import iyzipay
import requests
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from inoks.Forms.CargoForm import CargoForm
from inoks.Forms.OrderForm import OrderForm
from inoks.Forms.OrderFormAdmin import OrderFormAdmin
from inoks.Forms.OrderSituationsForm import OrderSituationsForm
from inoks.models import Order, OrderSituations, Profile, Product, OrderProduct, City, Settings, PaymentMethodPayTR, \
    PaymentMethodIyzico, IyzicoToken
from inoks.models.Cargo import Cargo
from inoks.models.CartObject import CartObject
from inoks.models.OrderObject import OrderObject
from inoks.models.UserProductObject import UserProductObject
from inoks.serializers.order_serializers import OrderSerializer
from inoks.serializers.product_cart_serializer import CartSerializer
from inoks.services import general_methods
from inoks.services.general_methods import activeOrder


@login_required
def return_add_orders_admin(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    kargo = float(Settings.objects.filter(name='kargo')[0].value)

    order_form = OrderFormAdmin(instance=Profile.objects.get(user=request.user))
    products = Product.objects.all()
    current_user = request.user
    profile = Profile.objects.get(user=current_user)

    if request.method == 'POST':

        order_form = OrderFormAdmin(request.POST)

        if order_form.is_valid():

            total_price = 0

            products_quantity = order_form.cleaned_data['droptxt']

            products_quantity = products_quantity.split(',')

            order_product_card = []

            order = Order(profile=order_form.cleaned_data['profile'],

                          city=order_form.cleaned_data['city'],
                          district=order_form.cleaned_data['district'],

                          address=order_form.cleaned_data['address'],
                          payment_type=order_form.cleaned_data['payment_type'],
                          isContract=order_form.cleaned_data['isContract'], otherAddress=request.POST['diger_adres'],
                          companyInfo=request.POST['kurumsal_bilgi'])
            order.isContract = order_form.cleaned_data['isContract']
            order.save()

            for products_q in products_quantity:
                product = products_q.split('x')
                prod = Product.objects.get(id=int(product[1].strip()))
                orderProduct = OrderProduct(order=order, product=prod,
                                            quantity=int(product[0].strip()))
                orderProduct.save()
                order_product_card.append(orderProduct)

                total_price = total_price + (int(product[0].strip()) * prod.price)
            if order.cargo.status:
                if total_price >= order.cargo.lower_limit:
                    order.totalPrice = total_price


                else:
                    # order.totalPrice = float(total_price) + kargo
                    order.totalPrice = float(total_price) + float(order.cargo.price)

                    order.save()

            # order.product.add(order_form.cleaned_data['product'])

            order.order_situations.add(OrderSituations.objects.get(name='Ödeme Bekliyor'))

            order.save()
            if order.payment_type == 'Havale/EFT':
                messages.success(request, 'Sipariş başarıyla eklendi.')
                return redirect('inoks:havale-eft-bilgi', siparis=order.id)

            else:

                messages.success(request, 'Sipariş başarıyla eklendi.')
                return redirect('inoks:odeme-yap', siparis=order.id)



        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'siparisler/siparis-ekle.html',
                  {'order_form': order_form, 'products': products, 'profile': profile, 'kargo': kargo})


@login_required
def return_add_orders(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    kargo = float(Settings.objects.filter(name='kargo')[0].value)
    products = Product.objects.all()
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    order_form = OrderForm(instance=Profile.objects.get(user=request.user),
                           initial={'address': profile.address, 'city': profile.city, 'district': profile.district})

    order_form.fields['city'].queryset = City.objects.filter(id=profile.city_id)

    if request.method == 'POST':

        order_form = OrderForm(request.POST)

        if order_form.is_valid():

            total_price = 0

            products_quantity = order_form.cleaned_data['droptxt']

            products_quantity = products_quantity.split(',')
            order_product_card = []

            order = Order(profile=profile,

                          city=order_form.cleaned_data['city'],
                          district=order_form.cleaned_data['district'],

                          address=order_form.cleaned_data['address'],
                          payment_type=order_form.cleaned_data['payment_type'],
                          isContract=order_form.cleaned_data['isContract'], otherAddress=request.POST['diger_adres'],
                          companyInfo=request.POST['kurumsal_bilgi'])
            order.isContract = order_form.cleaned_data['isContract']
            order.save()

            for products_q in products_quantity:
                product = products_q.split('x')
                prod = Product.objects.get(id=int(product[1].strip()))
                orderProduct = OrderProduct(order=order, product=prod,
                                            quantity=int(product[0].strip()))
                orderProduct.save()
                order_product_card.append(orderProduct)

                total_price = total_price + (int(product[0].strip()) * prod.price)

            if total_price >= 150:
                order.totalPrice = total_price
            else:
                order.totalPrice = float(total_price) + kargo

            order.save()

            # order.product.add(order_form.cleaned_data['product'])

            order.order_situations.add(OrderSituations.objects.get(name='Ödeme Bekliyor'))

            order.save()
            if order.payment_type == 'Havale/EFT':
                messages.success(request, 'Sipariş başarıyla eklendi.')
                return redirect('inoks:havale-eft-bilgi', siparis=order.id)

            else:

                messages.success(request, 'Sipariş başarıyla eklendi.')
                return redirect('inoks:odeme-yap', siparis=order.id)


        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'siparisler/siparis-ekle.html',
                  {'order_form': order_form, 'products': products, 'profile': profile, 'kargo': kargo})


@login_required
def return_add_orders_from_cart(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    kargo = float(Settings.objects.filter(name='kargo')[0].value)
    products = Product.objects.all()
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    order_form = OrderForm(initial={'address': profile.address, 'city': profile.city, 'district': profile.district,'guest_user':None})
    order_form.fields['city'].queryset = City.objects.filter(id=profile.city_id)

    myDict = dict(request.GET)
    urun_miktar = []
    urun_miktar_2 = []
    myDict2 = dict()

    for key in myDict:
        if key.startswith('cust'):
            pickup_dict = dict()
            x = myDict[key][0].split("&")
            x = CartObject(product_id=x[0], quantity=x[1])
            urun_miktar.append(x)
            pickup_dict['product_id'] = x.product_id
            pickup_dict['quantity'] = x.quantity
            urun_miktar_2.append(pickup_dict)

    myDict2['deneme'] = urun_miktar
    serializer = CartSerializer(urun_miktar, many=True)
    data = json.dumps(serializer.data)
    # data = serializers.serialize('json', myDict2)
    # serializer = CartSerializer(urun_miktar, many=True)

    # data = serializer.data

    if request.method == 'POST':

        order_form = OrderForm(request.POST)

        if order_form.is_valid():

            total_price = 0

            products_quantity = order_form.cleaned_data['droptxt']

            products_quantity = products_quantity.split(',')

            order_product_card = []

            order = Order(profile=profile,

                          city=order_form.cleaned_data['city'],
                          district=order_form.cleaned_data['district'],
                          address=order_form.cleaned_data['address'],
                          payment_type=order_form.cleaned_data['payment_type'],
                          isContract=order_form.cleaned_data['isContract'], otherAddress=request.POST['diger_adres'],
                          companyInfo=request.POST['kurumsal_bilgi'])
            order.isContract = order_form.cleaned_data['isContract']
            order.save()

            for products_q in products_quantity:
                product = products_q.split('x')
                prod = Product.objects.get(id=int(product[1].strip()))
                orderProduct = OrderProduct(order=order, product=prod,
                                            quantity=int(product[0].strip()))
                orderProduct.save()
                order_product_card.append(orderProduct)

                total_price = total_price + (int(product[0].strip()) * prod.price)

            if total_price >= 150:
                order.totalPrice = total_price
            else:
                order.totalPrice = float(total_price) + kargo

            order.save()

            # order.product.add(order_form.cleaned_data['product'])

            order.order_situations.add(OrderSituations.objects.get(name='Ödeme Bekliyor'))

            order.save()

            if order.payment_type == 'Havale/EFT':
                messages.success(request, 'Sipariş başarıyla eklendi.')
                return redirect('inoks:havale-eft-bilgi', siparis=order.id)

            else:

                messages.success(request, 'Sipariş başarıyla eklendi.')
                return redirect('inoks:odeme-yap', siparis=order.id)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'siparisler/siparis-ekle.html',
                  {'order_form': order_form, 'products': products, 'product_array': data, 'profile': profile,
                   'kargo': kargo})


@login_required
def return_pending_orders(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    pending_orders = Order.objects.filter(isApprove=False)
    order_situations = OrderSituations.objects.all()

    return render(request, 'siparisler/bekleyen-siparisler.html',
                  {'pending_orders': pending_orders, 'order_situations': order_situations})


@login_required
def return_orders(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    orders = Order.objects.filter(isApprove=True).order_by('-id')

    order_situations = OrderSituations.objects.all()
    return render(request, 'siparisler/siparisler.html', {'orders': orders, 'order_situations': order_situations})


@login_required
def return_order_situations(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    order_situations_form = OrderSituationsForm()

    if request.method == 'POST':

        order_situations_form = OrderSituationsForm(request.POST)

        if order_situations_form.is_valid():

            orderSituations = OrderSituations(name=order_situations_form.cleaned_data['name'])

            orderSituations.save()

            return redirect('inoks:siparis-durumlari')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    order_situations = OrderSituations.objects.all()
    return render(request, 'siparisler/siparis-durumlari.html',
                  {'order_situations_form': order_situations_form, 'order_situations': order_situations})


@login_required
def pending_order_delete(request, pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Order.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@api_view()
def getPendingOrder(request, pk):
    order = Order.objects.filter(pk=pk)

    data = OrderSerializer(order, many=True)

    responseData = {}
    responseData['pending_order'] = data.data
    responseData['pending_order'][0]
    return JsonResponse(responseData, safe=True)


@login_required
def pendingOrderActive(request):
    if request.POST:
        try:

            user_id = request.POST.get('user_id')

            activeOrder(request, int(user_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def return_my_orders(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    userprofile = Profile.objects.get(user=current_user)
    orderss = Order.objects.filter(profile_id=userprofile.id)

    orders = []

    for order in orderss:
        orderObject = OrderObject(order=order, total_price=0)
        orderObject.order = order
        orderObject.total_price = order.totalPrice
        orders.append(orderObject)

    return render(request, 'siparisler/siparislerim.html', {'orders': orders})


@api_view()
def getMyOrder(request, pk):
    order = Order.objects.filter(pk=pk)

    data = OrderSerializer(order, many=True)

    responseData = {}
    responseData['order'] = data.data
    responseData['order'][0]
    return JsonResponse(responseData, safe=True)


@login_required
def orders_delete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Order.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def orders_delete_member(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:

            obj = Order.objects.filter(profile__user=request.user).filter(pk=pk)
            if obj[0].payment_type == 'Kredi Kartı' and obj[0].order_situations.last().name == 'Ödeme Bekliyor':
                obj[0].delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@api_view()
def getOrder(request, pk):
    order = Order.objects.filter(pk=pk)

    data = OrderSerializer(order, many=True)

    responseData = {}
    responseData['order'] = data.data
    responseData['order'][0]
    return JsonResponse(responseData, safe=True)


@api_view(http_method_names=['POST'])
def siparis_durumu_guncelle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        isExist = False
        adSoyad = ''
        order_id = request.POST['order_id']
        situation_id = request.POST['situation_id']
        situation = OrderSituations.objects.get(pk=situation_id)
        order = Order.objects.get(pk=order_id)

        if len(order.order_situations.filter(name=situation.name)) > 0:
            order.order_situations.remove(situation)
            order.save()

        order.order_situations.add(situation)
        order.save()

        subject, from_email, to = 'BAVEN Sipariş Durumunuz Güncellendi ', 'info@baven.net', order.profile.user.email
        text_content = order_id + 'numaralı sipariş durumunuz güncellendi.'
        html_content = '<p> <strong>Site adresi:</strong> <a href="https://network.baven.net"></a>https://network.baven.net</p>'
        html_content = html_content + '<p><strong>Yeni Sipariş Durumu: </strong> ' + situation.name + '</p>'

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return JsonResponse({'status': 'Success', 'msg': 'Sipariş durumu güncellendi'})

    except Exception as e:

        return JsonResponse({'status': 'Fail', 'msg': 'Sipariş durumu güncellenmedi'})


def build_string(*args):
    return ''.join([str(a) for a in args])


def odemeYap(request, siparis):
    """perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')"""

    order = Order.objects.get(pk=siparis)
    payTr = PaymentMethodPayTR.objects.get(payment_type__name='Paytr')
    order_products = OrderProduct.objects.filter(order=order)

    user_basket = []

    for product in order_products:
        user_basket_content = []
        user_basket_content.append(product.product.name)
        user_basket_content.append(str(product.product.price))
        user_basket_content.append(str(product.quantity))
        user_basket.append(user_basket_content)

    """user_basket_content = []
    user_basket_content.append("Örnek ürün 1")
    user_basket_content.append("18.00")
    user_basket_content.append("1")

    user_basket_content2 = []
    user_basket_content2.append("Örnek ürün 2")
    user_basket_content2.append("18.00")
    user_basket_content2.append("1")
    user_basket.append(user_basket_content)
    # user_basket.append(user_basket_content2)"""

    encodedBytes = base64.b64encode(json.dumps(user_basket).encode())
    # encodedStr = str(encodedBytes, "utf-8")

    # data = base64.urlsafe_b64encode(json.dumps({'a': 123}).encode())

    merchant_id = payTr.merchantId
    merchant_key = payTr.merchantKey
    merchant_salt = payTr.merchantSalt
    #
    ## Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
    email = order.profile.user.email
    #
    ## Tahsil edilecek tutar.
    payment_amount = int(order.totalPrice * 100)
    # 9.99 için 9.99 * 100 = 999 gönderilmelidir.
    #
    ## Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    merchant_oid = order.id
    #
    ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
    user_name = order.profile.user.first_name + " " + order.profile.user.last_name
    #
    ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
    user_address = order.address
    #
    ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
    user_phone = order.profile.mobilePhone
    #
    ## Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
    ## !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    ## !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
    merchant_ok_url = "https://network.baven.net/baven/odeme-basarili/"
    #
    ## Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    ## !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    ## !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
    merchant_fail_url = "https://network.baven.net/baven/odeme-basarisiz/"
    #
    ## Müşterinin sepet/sipariş içeriği
    user_basket = encodedBytes.decode("utf-8")
    #
    # *ÖRNEK $user_basket oluşturma - Ürün adedine göre array'leri çoğaltabilirsiniz

    ############################################################################################

    ## Kullanıcının IP adresi

    ## !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
    ## buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
    user_ip = "78.177.33.217"
    ##

    ## İşlem zaman aşımı süresi - dakika cinsinden
    timeout_limit = "30"

    ## Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
    debug_on = 1

    ## Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    test_mode = 0

    no_installment = 0
    # // Taksityapılmasını istemiyorsanız, sadece tek çekim  sunacaksanız 1yapın

    ## Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
    ## Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
    max_installment = 0

    currency = "TL"

    hash_str = merchant_id + user_ip + str(merchant_oid) + email + str(payment_amount) + user_basket + str(
        no_installment) + str(max_installment) + currency + str(test_mode)

    """dig = hmac.new(
        b'Tw7p6HFLrbuyMRQ9', msg=hash_str + merchant_salt,
        digestmod=hashlib.sha256).hexdigest()
    paytr_token = base64.b64encode(bytes(binascii.hexlify(dig)))"""

    x = hash_str + merchant_salt
    dig = hmac.new('Tw7p6HFLrbuyMRQ9'.encode(), x.encode('utf-8'), hashlib.sha256)
    a = base64.b64encode(dig.digest()).decode()

    data = hash_str + merchant_salt
    message = bytes(hash_str + merchant_salt, 'utf-8')
    secret = bytes(merchant_key, 'utf-8')

    hash = hmac.new(secret, data.encode('utf-8'), hashlib.sha256)

    b = hash.digest()

    # to base64
    b = base64.b64encode(b).decode()

    hmac_hash = base64.b64encode(
        hmac.new(bytearray(merchant_key, 'utf-8'), data.encode('utf-8'), hashlib.sha256).digest())

    print(hmac_hash)

    # b = bytes(  merchant_key.encode('utf-8'))

    # h = hmac.new(b, hash_str + merchant_salt, hashlib.sha256).hexdigest()

    """paytr_token = base64.b64encode(
        hmac.new(hash_str + merchant_salt, merchant_key,  digestmod=hashlib.sha256).digest())"""

    parameters = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_amount': payment_amount,
        'paytr_token': b,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment': max_installment,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'timeout_limit': timeout_limit,
        'currency': currency,
        'test_mode': test_mode
    }

    response = requests.post("https://www.paytr.com/odeme/api/get-token", data=parameters, verify=False, timeout=90)

    return render(request, "odeme/odeme.html",
                  {"token": json.loads(response.text)['token'], "card": order_products, "total": order.totalPrice})


@csrf_exempt
def odeme_sonuc(request):
    post = request.POST

    merchant_key = 'Tw7p6HFLrbuyMBQ9'
    merchant_salt = 'HNZx6niqsJJjiiRq'

    data = str(request.POST.get("merchant_oid")) + merchant_salt + str(request.POST.get("status")) + str(
        request.POST.get("total_amount"))
    print(data)

    message = bytes(data, 'utf-8')
    secret = bytes(merchant_key, 'utf-8')

    hash = hmac.new(secret, data.encode('utf-8'), hashlib.sha256)

    b = hash.digest()

    # to base64
    b = base64.b64encode(b).decode()

    print(request.POST.get('merchant_oid'))
    order = Order.objects.get(pk=int(request.POST.get('merchant_oid')))

    if b != request.POST.get("hash"):
        sys.exit()

    if request.POST.get("status") == 'success':  ## Ödeme Onaylandı

        order.isPayed = True
        orderProducts = OrderProduct.objects.filter(order=order)
        for orderProduct in orderProducts:
            product = Product.objects.get(product=orderProduct.product)
            product.stock = product.stock - orderProduct.quantity
            product.save()
        order.order_situations.add(OrderSituations.objects.get(name="Onay Bekliyor"))
        order.save()

    else:
        order.delete()

    print("OK")

    response = HttpResponse()
    response.write("OK")

    return render(request, "odeme/odeme-bildirim.html", {"odeme": "OK"})


@csrf_exempt
def odeme_sonuc_iyzico(request):
    x = request
    iyzico = PaymentMethodIyzico.objects.get(payment_type__name='Iyzico')
    order_token = IyzicoToken.objects.get(token=x.POST.get('token')).order_id
    request = dict([('locale', 'tr')])
    request['conversationId'] = str(order_token.id)
    request['token'] = x.POST.get('token')
    order = Order.objects.get(pk=int(request['conversationId']))

    options = {

        'api_key': iyzico.apiKey,
        'secret_key': iyzico.secretKey,
        'base_url': iyzipay.base_url,
    }

    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    status = json.loads(checkout_form_result.read())['status']

    if status == "success":  ## Ödeme Onaylandı
        order.isPayed = True
        orderProducts = OrderProduct.objects.filter(order=order)
        for orderProduct in orderProducts:
            product = Product.objects.get(pk=orderProduct.product.pk)
            product.stock = product.stock - orderProduct.quantity
            product.save()
        order.order_situations.add(OrderSituations.objects.get(name="Onay Bekliyor"))
        order.save()

    else:
        order.delete()

    response = HttpResponse()
    response.write("OK")

    return render(request, "odeme/odeme-bildirim.html", {"odeme": "OK"})


def basarili_odeme(request):
    return render(request, 'odeme/basarili-odeme.html')


def basarisiz_odeme(request):
    return render(request, 'odeme/basarisiz-odeme.html')


def havale_eft(request, siparis):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    order = Order.objects.get(pk=siparis)
    order_products = OrderProduct.objects.filter(order=order)

    return render(request, 'odeme/havale-eft-bilgi.html',
                  {'card': order_products, 'siparis_no': siparis, "total": order.totalPrice})


def kargoBilgi(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    order = Order.objects.get(pk=pk)
    order_products = OrderProduct.objects.filter(order=order)

    return render(request, 'siparisler/kargo-bilgi.html',
                  {'card': order_products, 'siparis_no': pk, 'order': order, 'total': order.totalPrice,
                   'userOrder': order.profile})


@login_required
def cargo_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    cargo = Cargo.objects.get(pk=pk)
    cargo_form = CargoForm(request.POST or None, instance=cargo)
    if request.method == 'POST':
        if cargo_form.is_valid():
            cargo_form.save()

            messages.success(request, 'Başarıyla Güncellendi')

            return redirect('inoks:kargo-ücret-bilgileri')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    return render(request, 'kargo/kargo-guncelle.html',
                  {'cargo_form': cargo_form})


@login_required
def get_cargo(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    cargos = Cargo.objects.all()

    return render(request, 'kargo/kargo.html', {'cargos': cargos})


@login_required
def cargo_delete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    cargo = Cargo.objects.get(pk=pk)
    cargo.delete()
    messages.success(request, 'Kargo Bilgisi Silindi.')
    return redirect('inoks:kargo-ücret-bilgileri')
