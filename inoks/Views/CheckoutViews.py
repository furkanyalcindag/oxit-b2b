import base64
import hashlib
import hmac
import json
from decimal import Decimal
import requests
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives

from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.defaultfilters import floatformat
from django.template.loader import render_to_string

from inoks.Forms.AddressForm import AddressForm
from inoks.Forms.GuestUserForm import GuestUserForm
from inoks.Forms.LoginProfilForm import LoginProfilForm
from inoks.Forms.OrderUpdateForm import OrderForm
from inoks.Forms.UserCheckoutForm import UserCheckoutForm
from inoks.Forms.UserUpdateForm import UserUpdateForm
from inoks.models import Product, Profile, Settings, City, Order, OrderProduct, OrderSituations, PaymentType, \
    PaymentMethod, PaymentMethodPayTR
from inoks.models.Address import Address
from inoks.models.AddressObject import AddressObject
from inoks.models.AddressProfile import AddressProfile
from inoks.models.Cargo import Cargo
from inoks.models.Enum import ADDRESS_CHOISES, PAYMENT_CHOICES
from inoks.models.OrderProductObject import OrderProductObject
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
                   'kdv': kdv})


@login_required
def payment_info_islogin(request):
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
    payment_types = PaymentType.objects.all()
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
                   'kdv': kdv, 'kargo1': kargo1, 'addresses': address_dict, 'discount': discount,
                   'city': city, 'adres': address_title, 'payment_type': payment_types})


@login_required
def get_payment_info_isLogin(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)

    payment_type = request.POST['payment_type']
    paymentType = PaymentType.objects.get(name=payment_type)

    address_id = request.POST['address']
    adres = Address.objects.get(pk=address_id)
    address = adres.address
    address_city = adres.city
    address_district = adres.district

    subtotal = 0

    discount = 0
    net_total = 0
    total = 0
    kargo = Cargo.objects.get(name='Üzeri Kargo')
    kdv = Settings.objects.get(name='kdv')
    kargo1 = 0

    products = general_methods.products_in_card(json.loads(request.POST['card']))  # Sepetteki ürünler çağrılıyor

    for order in products:
        subtotal = order.subtotal + subtotal

    c_code = json.loads(request.POST['c_code'])

    if c_code == None:
        discount = discount

    else:
        code = c_code['c_code']
        discount = couponControl(code, subtotal)

    if products:
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

    order = Order()

    if request.POST['address-value'] == 'TRUE':  # fatura adresi = adres
        order.otherAddress = address
    else:
        order.otherAddress = request.POST['invoice_address']  # Farklı fatura adresi

    # siparis olusturuluyor
    order.payment_type = paymentType
    order.totalPrice = total
    order.cargo = kargo1
    order.profile = profile
    order.address = address
    order.city = address_city
    order.kdv = kdv
    order.discount = discount
    order.net_total = net_total

    order.district = address_district
    order.save()

    # siparişin ürünleri
    for product_order in products:
        product = Product.objects.get(pk=product_order.id)
        orderProduct = OrderProduct(order=order, product=product,
                                    quantity=product_order.count)
        orderProduct.save()

    """invoice_data = {'orders': products, 'subtotal': Decimal(subtotal), 'total': Decimal(total),
                    'net_total': Decimal(net_total), 'discount': discount,
                    'kdv': kdv, 'address': order.address, 'city': address_city, 'district': address_district,
                    'payment_type': order.payment_type, 'invoice_address': order.otherAddress, 'order': order,
                    'profile': profile}

    subject, from_email, to = 'Oxit Bilişim Teknolojileri', 'burcu.dogan@oxityazilim.com', current_user.email
    text_content = 'Fatura Bilgileri '

    html_body = render_to_string("mailTemplates/invoice2.html", invoice_data)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_body, "text/html")
    msg.send() """

    # stok guncelleme
    if orderProduct is not None:
        for product_order in products:
            product = Product.objects.get(pk=product_order.id)
            product.stock = product.stock - 1
            product.save()

    messages.success(request, 'Siparişiniz Başarıyla Oluştruldu.')

    if order.payment_type == 'Havale/EFT':
        messages.success(request, 'Sipariş başarıyla eklendi.')
        return redirect('inoks:havale-eft-bilgi', siparis=order.id)

    elif order.payment_type.name == 'Kredi Kartı':
        paymentMethod = PaymentMethod.objects.get(isActive=True)
        if paymentMethod.name == 'Paytr':
            messages.success(request, 'Sipariş başarıyla eklendi.')
            return redirect('inoks:kullanici-odeme-yap', siparis=order.id)


    else:

        return render(request, 'checkout/odeme-tamamla.html',
                      {'orders': products, 'subtotal': Decimal(subtotal), 'total': Decimal(total),
                       'net_total': Decimal(net_total),
                       'kdv': kdv, 'address': order.address, 'city': address_city, 'district': address_district,
                       'payment_type': order.payment_type, 'invoice_address': order.otherAddress})


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

    return render(request, "checkout/kullanici-odeme.html",
                  {"token": json.loads(response.text)['token'], "card": order_products, "order": order})


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
                 'il': il, 'a_id': adres.pk,
                 'message_type': 'success'
                 })

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': "Adres Eklenemedi", 'message_type': 'error'})
