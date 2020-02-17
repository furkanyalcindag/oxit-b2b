from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from inoks.Forms.ProfileCreditCardForm import ProfileCreditCardForm
from inoks.Forms.UserForm import UserForm
from inoks.Forms.ProfileForm import ProfileForm
from inoks.Forms.ProfileUpdateForm import ProfileUpdateForm
from inoks.Forms.ProfileUpdateMemberForm import ProfileUpdateMemberForm
from inoks.Forms.UserUpdateForm import UserUpdateForm
from inoks.models import Profile
from inoks.models.CreditCardObject import CreditCardObject
from inoks.models.CreditCard import CreditCard
from inoks.models.ProfileCreditCard import ProfileCreditCard
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

    return render(request, 'kullanici/kullanici-ekle.html', {'user_form': user_form, 'profile_form': profile_form})


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

    return render(request, 'kullanici/kullanici-kredi-kart-ekle.html',
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

    return render(request, 'kullanici/kullanici-kredi-kart-guncelle.html',
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

    return render(request, 'kullanici/kullanici-ekle.html',
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

    return render(request, 'kullanici/kullanici-bilgileri.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'ilce': profile.district})


@login_required
def return_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    users = Profile.objects.filter(user__is_active=True).filter(~Q(user__groups__name='Admin'))

    return render(request, 'kullanici/kullanicilar.html', {'users': users})


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

    return render(request, 'kullanici/kullanici-bilgi.html', {'password': password, 'username': user.username})


@login_required
def return_my_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    userprofile = Profile.objects.get(user=current_user)

    users = Profile.objects.filter(sponsor_id=userprofile.id, isApprove=True)

    return render(request, 'kullanici/uyelerim.html', {'users': users})


@login_required
def return_pending_users(request):
    if request.user.groups.all()[0] != Group.objects.get(name="Admin"):
        logout(request)
        return redirect('accounts:login')
    users = Profile.objects.filter(isApprove=False)

    return render(request, 'kullanici/bekleyen-kullanicilar.html', {'users': users})


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

    return render(request, 'kullanici/iptal-edilen-kullanicilar.html', {'users': users})
