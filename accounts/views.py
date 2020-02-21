from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group, Permission
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth, messages

# Create your views here.
from accounts.forms import ResetPassword
from inoks import urls
from inoks.Forms.ProfileFormForMember import ProfileForm
from education.Forms.UserForm import UserForm
from inoks.models import Profile
from inoks.services import general_methods


def index(request):
    return render(request, 'accounts/index.html')


# def login(request):
# return render(request, 'registration/login.html')


def login(request):
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
                return redirect('inoks:user-dashboard')

            else:
                return redirect('accounts:logout')

        else:
            messages.add_message(request, messages.SUCCESS, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        obj = User.objects.filter(username=mail)
        if obj.count() != 0:
            obj = obj[0]
            password = User.objects.make_random_password()
            obj.set_password(password)
            # form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
            user = obj.save()
            html_content = ''
            subject, from_email, to = 'BAVEN Kullanıcı Bilgileri', 'info@baven.net', obj.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong> <a href="http://185.122.203.112/"></a>baven.net</p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı:</strong>' + obj.username + '</p>'
            html_content = html_content + '<p><strong>Şifre:</strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
            return redirect("accounts:login")
        else:
            messages.warning(request, "Geçerli bir mail adresi giriniz.")
            return redirect("accounts:forgot")

    return render(request, 'registration/forgot.html')


def pagelogout(request):
    logout(request)
    return redirect('accounts:login')


def register_member(request):
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
                             job=profile_form.cleaned_data['job'],
                             city=profile_form.cleaned_data['city'],
                             educationLevel=profile_form.cleaned_data['educationLevel'],
                             mobilePhone=profile_form.cleaned_data['mobilePhone'],
                             birthDate=profile_form.cleaned_data['birthDate'],
                             district=profile_form.cleaned_data['district'],
                             sponsor=profile_form.cleaned_data['sponsor'],
                             iban=profile_form.cleaned_data['iban'],
                             ibanAdSoyad=profile_form.cleaned_data['ibanAdSoyad'],
                             )

            profil.sponsor = profile_form.cleaned_data['sponsor']
            profil.isContract = profile_form.cleaned_data['isContract']
            profil.isApprove = True
            profil.isActive = True
            sponsorNumber = Profile.objects.filter(sponsor=profile_form.cleaned_data['sponsor']).count()
            sp_profile = Profile.objects.get(pk=profile_form.cleaned_data['sponsor'].pk)
            limit = 0

            if sp_profile.user.groups.all()[0].name == 'Admin':
                limit = 9
            else:
                limit = 2

            if sponsorNumber > limit:
                messages.warning(request, 'Üyeye Sponsor Eklenemez. Sponsor Alanı Dolmuştur.')
                user.delete()
                return redirect('accounts:register')
            else:
                profil.save()

                subject, from_email, to = 'Baven Kullanıcı Giriş Bilgileri', 'info@baven.net', user2.email
                text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
                html_content = '<p> <strong>Site adresi:</strong> <a href="https://network.bavev.net"></a>network.baven.net</p>'
                html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
                html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, 'Üye Başarıyla Kayıt Edilmiştir.')

                return redirect('accounts:login')

        else:
            isExist = general_methods.existMail(data['email'])
            if isExist:
                messages.warning(request, 'Mail adresi başka bir üyemiz tarafından kullanılmaktadır.')

            for x in profile_form.errors.as_data():
                messages.warning(request, profile_form.errors[x][0])

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})


def groups(request):
    group = Group.objects.all()

    return render(request, 'permission/groups.html', {'groups': group})


@login_required
def permission(request, pk):
    general_methods.show_urls(urls.urlpatterns, 0)
    group = Group.objects.get(pk=pk)
    menu = ""
    ownMenu = ""

    groups = group.permissions.all()
    per = []
    menu2 = []

    for gr in groups:
        per.append(gr.codename)

    ownMenu = group.permissions.all()

    menu = Permission.objects.all()

    for men in menu:
        if men.codename in per:
            print("echo")
        else:
            menu2.append(men)

    return render(request, 'permission/izin-ayar.html',
                  {'menu': menu2, 'ownmenu': ownMenu, 'group': group})


@login_required
def permission_post(request):
    if request.POST:
        try:
            permissions = request.POST.getlist('values[]')
            group = Group.objects.get(pk=request.POST.get('group'))

            group.permissions.clear()
            group.save()
            if len(permissions) == 0:
                return JsonResponse({'status': 'Success', 'messages': 'Sınıf listesi boş'})
            else:
                for id in permissions:
                    perm = Permission.objects.get(pk=id)
                    group.permissions.add(perm)

            group.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Permission.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def change_password(request):
    if request.method == 'POST':
        form = ResetPassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Şifreniz başarıyla değiştirilmiştir.')
            return redirect('accounts:change_password')
        else:
            for error in form.errors.keys():
                messages.warning(request, form.errors[error])

    else:
        form = ResetPassword(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
