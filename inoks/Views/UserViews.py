from django.contrib import messages, auth
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

from accounts.forms import ResetPassword
from inoks.Forms.AddressForm import AddressForm
from inoks.Forms.LoginProfilForm import LoginProfilForm
from inoks.Forms.LoginProfilUpdateForm import LoginProfileUpdateForm
from inoks.Forms.LoginUserForm import LoginUserForm
from inoks.Forms.ProfileCreditCardForm import ProfileCreditCardForm
from inoks.Forms.RefundForm import RefundForm
from inoks.Forms.UserForm import UserForm
from inoks.Forms.ProfileForm import ProfileForm
from inoks.Forms.ProfileUpdateForm import ProfileUpdateForm
from inoks.Forms.ProfileUpdateMemberForm import ProfileUpdateMemberForm
from inoks.Forms.UserUpdateForm import UserUpdateForm
from inoks.models import Profile, Settings, Order, Refund, OrderProduct, Notification, Rating
from inoks.models.Address import Address
from inoks.models.AddressObject import AddressObject
from inoks.models.AddressProfile import AddressProfile
from inoks.models.CreditCardObject import CreditCardObject
from inoks.models.CreditCard import CreditCard
from inoks.models.Enum import ADDRESS_CHOISES
from inoks.models.OrderObject import OrderObject
from inoks.models.ProfileCreditCard import ProfileCreditCard
from inoks.models.RefundObject import RefundObject
from inoks.serializers.profile_serializers import ProfileSerializer
from inoks.services import general_methods
from inoks.services.general_methods import activeUser, passiveUser, reactiveUser


@login_required
def return_add_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    profile_form = ProfileForm()

    if request.method == 'POST':
        x = User.objects.latest('id')

        data = request.POST.copy()
        data['username'] = data['email']
        user_form = UserForm(data)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            group = Group.objects.get(name='Üye')
            user2 = user_form.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user2.groups.add(group)
            user.is_active = True
            user.save()

            profil = Profile(user=user, tc=profile_form.cleaned_data['tc'],
                             profileImage=profile_form.cleaned_data['profileImage'],
                             address=profile_form.cleaned_data['address'],
                             gender=profile_form.cleaned_data['gender'],
                             city=profile_form.cleaned_data['city'],
                             mobilePhone=profile_form.cleaned_data['mobilePhone'],
                             birthDate=profile_form.cleaned_data['birthDate'],
                             district=profile_form.cleaned_data['district'],
                             )

            profil.isContract = profile_form.cleaned_data['isContract']
            profil.isApprove = True
            profil.isActive = True

            profil.save()

            subject, from_email, to = 'BAVEN Kullanıcı Giriş Bilgileri', 'info@baven.net', user2.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong> <a href="https://network.baven.net">network.baven.net</a></p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
            html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Üye Başarıyla Kayıt Edilmiştir.')

            return redirect('inoks:kullanici-ekle')

        else:
            isExist = general_methods.existMail(data['email'])
            if isExist:
                messages.warning(request, 'Mail adresi başka bir üyemiz tarafından kullanılmaktadır.')

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'bayi/kullanici-ekle.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def return_add_user_creditcart(request, pk):
    user = User.objects.get(id=pk)
    perm = general_methods.control_access(request)
    if not perm and request.user == user:
        logout(request)
        return redirect('accounts:login')
    user_card_form = ProfileCreditCardForm(request.POST)

    profile = Profile.objects.get(user=user)

    creditCards = []
    cards = ProfileCreditCard.objects.filter(profile=profile)

    for card in cards:
        cardObject = CreditCardObject(id=0, cardNumber=None, cvv=None, name=None, card_name_lastName=None)
        number = ''
        cvv_number = ''
        for x in range(len(card.creditCard.cartNumber)):
            if x == 0 or x == 1 or x == 2 or x == 3 or x == 4 or x == 5 or x == 6:
                number = number + card.creditCard.cartNumber[x]
            else:
                number = number + '*'
        for x in range(len(card.creditCard.cvv)):
            if x == 0 or x == 2:
                cvv_number = cvv_number + card.creditCard.cvv[x]
            else:
                cvv_number = cvv_number + '*'

        cardObject.cardNumber = number
        cardObject.name = card.creditCard.name
        cardObject.card_name_lastName = card.creditCard.card_name_lastName
        cardObject.cvv = cvv_number
        cardObject.id = card.creditCard.pk
        creditCards.append(cardObject)

    if request.method == 'POST':

        if user_card_form.is_valid():

            userCard = CreditCard(name=user_card_form.cleaned_data['name'],
                                  cvv=user_card_form.cleaned_data['cvv'],
                                  cartNumber=user_card_form.cleaned_data['cartNumber'],
                                  card_name_lastName=user_card_form.cleaned_data['card_name_lastName'])
            userCard.save()
            creditCardUser = ProfileCreditCard(profile=profile, creditCard=userCard)
            creditCardUser.save()

            return redirect('inoks:kullanici-kart-ekle', pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'bayi/kullanici-kredi-kart-ekle.html',
                  {'card_form': user_card_form, 'cards': creditCards})


@login_required
def credit_card_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    creditCard = CreditCard.objects.get(pk=pk)
    card_form = ProfileCreditCardForm(request.POST or None)

    if request.method == 'POST':

        if card_form.is_valid():

            creditCard.name = card_form.cleaned_data['name']
            creditCard.cvv = card_form.cleaned_data['cvv']
            creditCard.card_name_lastName = card_form.cleaned_data['card_name_lastName']
            creditCard.cartNumber = card_form.cleaned_data['cartNumber']

            card_form.save()
            creditCardUser = ProfileCreditCard(creditCard=card_form)
            creditCardUser.save()

            messages.success(request, 'Kredi Kartı Bilgileri Başarıyla Güncellenmiştir.')
            return redirect('inoks:kullanici-kart-guncelle', pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'bayi/kullanici-kredi-kart-guncelle.html',
                  {'card_form': card_form})


@login_required
def credit_card_delete(request, pk):
    card = CreditCard.objects.get(pk=pk)
    obj = ProfileCreditCard.objects.filter(creditCard=card)
    obj.delete()
    return redirect('inoks:kullanicilar')


@login_required
def users_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    user = User.objects.get(id=pk)

    user_form = UserUpdateForm(request.POST or None, instance=user)
    profile = Profile.objects.get(user=user)
    profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.username = user_form.cleaned_data['email']
            user.is_active = True
            user.save()
            profile_form.save()

            messages.success(request, 'Profil Bilgileriniz Başarıyla Güncellenmiştir.')
            return redirect('inoks:user-dashboard')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'bayi/kullanici-ekle.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'ilce': profile.district})


@login_required
def users_information(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    user = User.objects.get(pk=pk)

    user_form = UserUpdateForm(request.POST or None, instance=user)
    profile = Profile.objects.get(user=user)
    profile_form = ProfileUpdateMemberForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.is_active = True
            user.save()
            profile_form.save()

            messages.success(request, 'Profil Bilgileriniz Başarıyla Güncellenmiştir.')
            return redirect('inoks:user-dashboard')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'bayi/kullanici-bilgileri.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'ilce': profile.district})


@login_required
def return_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    users = Profile.objects.filter(user__is_active=True).filter(~Q(user__groups__name='Admin'))

    return render(request, 'bayi/kullanicilar.html', {'users': users})


@login_required
def send_information(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = User.objects.get(pk=pk)
    password = User.objects.make_random_password()
    user.set_password(password)
    user.save()

    subject, from_email, to = 'Baven Kullanıcı Giriş Bilgileri', 'info@baven.net', user.email
    text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
    html_content = '<p> <strong>Site adresi:</strong> <a href="https://network.bavev.net"></a>network.baven.net</p>'
    html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user.username + '</p>'
    html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return render(request, 'bayi/kullanici-bilgi.html', {'password': password, 'username': user.username})


@login_required
def return_my_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    userprofile = Profile.objects.get(user=current_user)

    users = Profile.objects.filter(sponsor_id=userprofile.id, isApprove=True)

    return render(request, 'bayi/uyelerim.html', {'users': users})


@login_required
def return_pending_users(request):
    if request.user.groups.all()[0] != Group.objects.get(name="Admin"):
        logout(request)
        return redirect('accounts:login')
    users = Profile.objects.filter(isApprove=False)

    return render(request, 'bayi/bekleyen-kullanicilar.html', {'users': users})


@api_view()
def getPendingProfile(request, pk):
    profile = Profile.objects.filter(pk=pk)

    data = ProfileSerializer(profile, many=True)

    responseData = {}
    responseData['profile'] = data.data
    responseData['profile'][0]
    return JsonResponse(responseData, safe=True)


@api_view()
def getAllProfile(request, pk):
    profile = Profile.objects.filter(pk=pk)

    data = ProfileSerializer(profile, many=True)

    responseData = {}
    responseData['profile'] = data.data
    responseData['profile'][0]
    return JsonResponse(responseData, safe=True)


@api_view()
def getDeactiveProfile(request, pk):
    profile = Profile.objects.filter(pk=pk)

    data = ProfileSerializer(profile, many=True)

    responseData = {}
    responseData['profile'] = data.data
    responseData['profile'][0]
    return JsonResponse(responseData, safe=True)


@login_required
def profile_active_passive(request):
    if request.POST:
        try:

            user_id = request.POST.get('user_id')

            activeUser(request, int(user_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def profile_reactive(request):
    if request.POST:
        try:

            user_id = request.POST.get('user_id')

            reactiveUser(request, int(user_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def profile_passive(request):
    if request.POST:
        try:

            user_id = request.POST.get('user_id')

            passiveUser(request, int(user_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def pending_profile_delete(request, pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Profile.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_deactive_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    users = Profile.objects.filter(isActive=False)

    return render(request, 'bayi/iptal-edilen-kullanicilar.html', {'users': users})


def user_register(request):
    user_form = LoginUserForm(request.POST or None)
    profile_form = LoginProfilForm(request.POST or None)
    contract = Settings.objects.get(name='Sozlesme')

    if request.method == 'POST':

        data = request.POST.copy()
        data['username'] = data['email']

        if user_form.is_valid() and profile_form.is_valid():

            if request.POST['password'] == request.POST['confirm_password']:
                user = user_form.save(commit=False)
                user.username = user.email
                user.save()
                group = Group.objects.get(name='Üye')
                user2 = user_form.save()
                user2.groups.add(group)
                user.save()
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                profil = Profile(user=user, mobilePhone=profile_form.cleaned_data['mobilePhone'])
                profil.isContract = profile_form.cleaned_data['isContract']
                profil.isNotification = profile_form.cleaned_data['isNotification']
                profil.save()
                messages.success(request, 'Kullanıcı Kaydedildi.Giriş Yapabilirsiniz.')
                return redirect('inoks:kullanici-giris')


            else:
                messages.warning(request, 'Girdiğiniz şifreler eşleşmemektedir.')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-ekle.html',
                  {'profile_form': profile_form, 'user_form': user_form, 'contract': contract})


def user_login(request):
    if request.user.is_authenticated is True:
        return redirect('inoks:admin-dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)

            if user.groups.all()[0].name == 'Admin':
                return redirect('inoks:admin-dashboard')

            elif user.groups.all()[0].name == 'Üye':

                return redirect('inoks:kullanici-urun-sayfasi')

            # logout yapılcak
        else:
            messages.add_message(request, messages.WARNING, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return render(request, 'kullanici/kullanici-login.html')

    return render(request, 'kullanici/kullanici-login.html')


def user_logout(request):
    logout(request)
    return redirect('inoks:kullanici-giris')


def user_profil(request):
    user = request.user
    user_form = UserUpdateForm(request.POST or None, instance=user)
    profile = Profile.objects.get(user=user)
    profile_form = LoginProfileUpdateForm(request.POST or None, instance=profile)

    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.username = user_form.cleaned_data['email']
            profile.mobilePhone = profile_form.cleaned_data['mobilePhone']

            user.save()
            profile_form.save()

            messages.success(request, 'Profil Bilgileriniz Başarıyla Güncellenmiştir.')
            return redirect('inoks:kullanici-profil')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-hesabi.html', {'user_form': user_form, 'profile_form': profile_form})


def user_change_password(request):
    if request.method == 'POST':
        form = ResetPassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Şifreniz başarıyla değiştirilmiştir.')
            return redirect('inoks:kullanici-profil')
        else:
            for error in form.errors.keys():
                messages.warning(request, form.errors[error])

    else:
        form = ResetPassword(request.user)
    return render(request, 'kullanici/kullanici-sifre-guncelle.html', {'form': form})


@login_required
def user_my_orders(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    userprofile = Profile.objects.get(user=current_user)
    orderss = Order.objects.filter(profile_id=userprofile.id)

    orders = []

    for order in orderss:
        order_product = OrderProduct.objects.filter(order=order)
        orderObject = OrderObject(order=order, total_price=0)
        orderObject.total_price = order.totalPrice
        orders.append(orderObject)

    return render(request, 'kullanici/kullanici-siparisleri.html', {'orders': orders})


def user_products(request, pk):
    order = Order.objects.get(pk=pk)
    order_product = OrderProduct.objects.filter(order=order)
    ratings = Rating.objects.all()

    return render(request, 'kullanici/kullanici-siparis-urunleri.html',
                  {'order_product': order_product, 'orders': order, 'ratings': ratings})


@login_required
def add_user_address(request):
    current_user = request.user

    perm = general_methods.control_access(request)
    if not perm and request.user == current_user:
        logout(request)
        return redirect('accounts:login')

    address_form = AddressForm(request.POST)

    profile = Profile.objects.get(user=current_user)

    addresses = AddressProfile.objects.filter(profile=profile)

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
            return redirect('inoks:kullanici-adres-ekle')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-adres-ekle.html',
                  {'address_form': address_form})


@login_required
def get_address(request):
    current_user = request.user
    perm = general_methods.control_access(request)
    if not perm and request.user == current_user:
        logout(request)
        return redirect('accounts:login')

    profile = Profile.objects.get(user=current_user)

    addresses = AddressProfile.objects.filter(profile=profile)
    address_dict = dict()

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

    return render(request, 'kullanici/kullanici-adres-bilgileri.html', {'addresses': address_dict})


def user_add_refund(request):  # Kulanıcı İade Oluştur
    """" perm = general_methods.control_access(request)

     if not perm:
         logout(request)
         return redirect('accounts:login')"""
    refund_form = RefundForm()
    email = ""
    if request.method == 'POST':

        refund_form = RefundForm(request.POST, request.FILES)

        if refund_form.is_valid():

            refund = Refund(order=refund_form.cleaned_data['order'],
                            product=refund_form.cleaned_data['product'],
                            orderQuantity=refund_form.cleaned_data['orderQuantity'],
                            isOpen=refund_form.cleaned_data['isOpen'],
                            )
            refund.save()

            refund.refundSituations.add(refund_form.cleaned_data['refundSituations'])

            refund.save()
            notification = Notification()
            notification.key = "kullanici iade"
            if refund.order.isGuest:
                notification.message = refund.order.guestUser.firstName + ' ' + refund.order.guestUser.lastName + ' ' + refund.product.code + 'kodlu ürünü iade etmek istiyor.(Misafir Kullanıcı)'
                email = refund.order.guestUser.email
            else:
                notification.message = refund.order.profile.user.first_name + ' ' + refund.order.profile.user.last_name + ' ' + refund.product.code + ' kodlu ürünü iade etmek istiyor'
                email = refund.order.profile.user.email
            notification.save()
            invoice_data = {'refund_id': refund.id}

            subject, from_email, to = 'Oxit Bilişim Teknolojileri', 'burcu.dogan@oxityazilim.com', email
            text_content = 'İade Bilgisi'

            html_body = render_to_string("mailTemplates/refund.html", invoice_data)

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_body, "text/html")
            msg.send()

            messages.success(request, 'Mesajınız başarıyla alınmıştır.En yakın sürede dönüş sağlanacaktır.')
        else:
            messages.warning(request, 'Üznünüz bir hata oluştu.Lütfen mesajınızı yeniden gönderin.')

            return redirect('inoks:kullanici-iade-olustur')

    return render(request, 'kullanici/kullanici-iade-olustur.html', {'refund_form': refund_form})


@login_required
def user_my_refunds(request):
    """ perm = general_methods.control_access(request)

     if not perm:
         logout(request)
         return redirect('accounts:login')"""
    refundList = []
    current_user = request.user
    refund = Profile.objects.get(user=current_user)
    refund_list = Refund.objects.filter(order__profile_id=refund)
    return render(request, 'kullanici/kullanici-urun-iade.html', {'refund_list': refund_list})


def guest_my_refunds(request):
    refund_list = []
    if request.POST:
        refund = request.POST['guestRefund']
        refund_list = Refund.objects.get(pk=refund)
        return render(request, 'kullanici/misafirKullanici-urun-iade.html', {'refund_list': refund_list})

    return render(request, 'kullanici/misafirKullanici-iade-sorgula.html', {'refund_list': refund_list})


@login_required
def user_delete_address(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    address = Address.objects.get(pk=pk)
    adresProfile = AddressProfile.objects.get(address=address)
    adresProfile.delete()
    address.delete()
    return redirect('inoks:kullanici-adres-bilgileri')


@login_required
def user_address_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user

    profile = Profile.objects.get(user=user)
    address = Address.objects.get(pk=pk)
    address_form = AddressForm(request.POST or None, instance=address)

    if request.method == 'POST':

        if address_form.is_valid():
            address_form.save()

            messages.success(request, 'Adres Bilgileri Başarıyla Güncellenmiştir.')
            return redirect('inoks:kullanici-adres-guncelle', pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-adres-guncelle.html',
                  {'address_form': address_form, 'ilce': address.district})
