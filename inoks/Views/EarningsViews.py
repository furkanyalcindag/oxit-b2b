import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect

from inoks.models import Order, Profile, earningPayments
from inoks.models.TotalOrderObject import TotalOrderObject
from inoks.services import general_methods
from inoks.services.general_methods import calculate_order_of_tree


@login_required
def return_my_earnings_report(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    userprofile = Profile.objects.filter(user=request.user)
    earnDict = dict()
    earningArray = []
    total = float(0.00)
    total_paid = 0
    not_paid = 0
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    part = str(month) + "/" + str(year)
    total_paid = general_methods.monthlyTotalPaidByDate(str(month), str(year))
    for user in userprofile:

        profileArray = []
        levelDict = dict()
        level = 1
        total_earning = 0

        profileArray.append(user.id)

        general_methods.returnLevelTree(profileArray, levelDict, level)

        # for i in range(7):
        #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

        order_total_member = general_methods.monthlyMemberOrderTotal(user)

        total_earning = general_methods.calculate_earning_of_tree(levelDict, order_total_member)
        # earnDict[user] = total_earning
        x = total_earning
        earnDict[user] = x - (x * 20 / 100)
        total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                        tree_price=0, kdv_tree_price=0, income_tax_tree_price=0, total_earn_with_tax=0)
        total_object.profile = user
        total_object.earning = earnDict[user]
        total_object.total_price = general_methods.monthlyMemberOrderTotal(user, )

        total_object.tree_price = total_earning
        # total_object.kdv_tree_price = total_earning - x
        total_object.income_tax_price = (x * 20 / 100)
        payment = earningPayments.objects.filter(profile=user,
                                                 payedDate=part)
        if payment.count() > 0:
            total_object.is_paid = True
            total_object.paid_date = payment[0].creationDate

        earningArray.append(total_object)

    for key in earnDict:
        total = total + float(earnDict[key])

    if request.method == 'POST':
        userprofile = Profile.objects.filter(user=request.user)
        earnDict = dict()
        earningArray = []
        total = 0
        total_paid = 0
        not_paid = 0

        total_paid = general_methods.monthlyTotalPaidByDate(request.POST['ay'], request.POST['yil'])

        part = request.POST['ay'] + "/" + request.POST['yil']

        for user in userprofile:

            profileArray = []
            levelDict = dict()
            level = 1
            total_earning = 0

            profileArray.append(user.id)

            general_methods.returnLevelTreeByDate(profileArray, levelDict, level, int(request.POST['ay']),
                                                  int(request.POST['yil']))

            # for i in range(7):
            #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))
            order_total_member = general_methods.monthlyMemberOrderTotal(user)

            total_earning = general_methods.calculate_earning_of_tree(levelDict, order_total_member)
            x = total_earning
            earnDict[user] = x - (x * 20 / 100)
            total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                            tree_price=0, kdv_tree_price=0, income_tax_tree_price=0,
                                            total_earn_with_tax=0)
            total_object.profile = user
            total_object.earning = earnDict[user]
            total_object.total_price = general_methods.monthlyMemberOrderTotalByDate(user, int(request.POST['ay']),
                                                                                     int(request.POST['yil']))
            total_object.tree_price = calculate_order_of_tree(levelDict)
            # total_object.kdv_tree_price = total_earning - x
            total_object.income_tax_price = (x * 20 / 100)
            total_object.total_earn_with_tax = total_earning

            payment = earningPayments.objects.filter(profile=user,
                                                     payedDate=request.POST['ay'] + "/" + request.POST['yil'])
            if payment.count() > 0:
                total_object.is_paid = True
                total_object.paid_date = payment[0].creationDate


            earningArray.append(total_object)

        for key in earnDict:
            total = total + float(earnDict[key])

        return render(request, 'kazanclar/kazanclarim.html',
                      {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                       'not_paid': float(total) - float(total_paid),
                       'part': part, 'month': request.POST['ay'], 'year': request.POST['yil']})
    return render(request, 'kazanclar/kazanclarim.html',
                  {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                   'not_paid': float(total) - float(total_paid),
                   'part': part, 'month': str(month), 'year': str(year)})


@login_required
def return_all_earnings_report(request):
    total_my_orders = Order.objects.filter(isApprove=True).count()
    orders = Order.objects.filter(isApprove=True)

    return render(request, 'kazanclar/kazanclar.html', {'orders': orders, 'total_my_orders': total_my_orders})


@login_required
def return_odenenler(request):
    return render(request, 'kazanclar/odenenler.html')


@login_required
def return_odenecekler(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    userprofile = Profile.objects.filter(user__is_active=True).exclude(user__groups__name="Admin")
    earnDict = dict()
    earningArray = []
    total = float(0.00)
    total_paid = 0
    not_paid = 0
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    part = str(month) + "/" + str(year)
    total_paid = general_methods.monthlyTotalPaidByDate(str(month), str(year))
    for user in userprofile:

        profileArray = []
        levelDict = dict()
        level = 1
        total_earning = 0

        profileArray.append(user.id)

        general_methods.returnLevelTree(profileArray, levelDict, level)

        # for i in range(7):
        #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

        order_total_member = general_methods.monthlyMemberOrderTotal(user, )

        total_earning = general_methods.calculate_earning_of_tree(levelDict, order_total_member)

        # earnDict[user] = total_earning
        # x = (total_earning * 100) / 118
        x = total_earning
        earnDict[user] = x - (x * 20 / 100)
        total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                        tree_price=0, kdv_tree_price=0, income_tax_tree_price=0, total_earn_with_tax=0)
        total_object.profile = user
        total_object.earning = earnDict[user]
        total_object.total_price = order_total_member

        total_object.tree_price = total_earning
        # total_object.kdv_tree_price = total_earning - x
        total_object.income_tax_price = (x * 20 / 100)

        payment = earningPayments.objects.filter(profile=user,
                                                 payedDate=part)
        if payment.count() > 0:
            total_object.is_paid = True
            total_object.paid_date = payment[0].creationDate

        earningArray.append(total_object)

    for key in earnDict:
        total = total + float(earnDict[key])

    if request.method == 'POST':
        userprofile = Profile.objects.filter(user__is_active=True).exclude(user__groups__name="Admin")
        earnDict = dict()
        earningArray = []
        total = 0
        total_paid = 0
        not_paid = 0

        total_paid = general_methods.monthlyTotalPaidByDate(request.POST['ay'], request.POST['yil'])

        part = request.POST['ay'] + "/" + request.POST['yil']

        for user in userprofile:

            profileArray = []
            levelDict = dict()
            level = 1
            total_earning = 0

            profileArray.append(user.id)

            general_methods.returnLevelTreeByDate(profileArray, levelDict, level, int(request.POST['ay']),
                                                  int(request.POST['yil']))

            # for i in range(7):
            #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

            order_total_member = general_methods.monthlyMemberOrderTotalByDate(user, int(request.POST['ay']),
                                                                               int(request.POST['yil']))

            total_earning = general_methods.calculate_earning_of_tree(levelDict, order_total_member)

            # earnDict[user] = total_earning
            # x = (total_earning * 100) / 118
            x = total_earning
            earnDict[user] = x - (x * 20 / 100)
            total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                            tree_price=0, kdv_tree_price=0, income_tax_tree_price=0,
                                            total_earn_with_tax=0)
            total_object.profile = user
            total_object.earning = earnDict[user]
            total_object.total_price = order_total_member
            total_object.tree_price = calculate_order_of_tree(levelDict)
            # total_object.kdv_tree_price = total_earning - x
            total_object.income_tax_price = (x * 20 / 100)
            total_object.total_earn_with_tax = total_earning

            payment = earningPayments.objects.filter(profile=user,
                                                     payedDate=request.POST['ay'] + "/" + request.POST['yil'])
            if payment.count() > 0:
                total_object.is_paid = True
                total_object.paid_date = payment[0].creationDate

            earningArray.append(total_object)

        for key in earnDict:
            total = total + float(earnDict[key])

        return render(request, 'kazanclar/odenecekler.html',
                      {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                       'not_paid': float(total) - float(total_paid),
                       'part': part, 'month': request.POST['ay'], 'year': request.POST['yil']})

    return render(request, 'kazanclar/odenecekler.html',
                  {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                   'not_paid': float(total) - float(total_paid),
                   'part': part, 'month': str(month), 'year': str(year)})


def calculate_earning(request):
    userprofile = Profile.objects.filter(user__is_active=True)

    earnDict = dict()

    for user in userprofile:

        profileArray = []
        levelDict = dict()
        level = 1
        total_earning = 0

        profileArray.append(user.id)

        general_methods.returnLevelTree(profileArray, levelDict, level)

        for i in range(7):
            total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

        earnDict[user] = total_earning


@login_required
def make_pay(request):
    if request.POST:
        try:

            profile_id = request.POST.get('profile_id')
            user = request.user
            part = request.POST.get('part')
            payment = request.POST.get('payment')

            payment = earningPayments(profile=Profile.objects.get(id=profile_id),
                                      payer_profile=Profile.objects.get(user=user),
                                      payedDate=part,
                                      paymentTotal=payment)

            payment.save()

            subject, from_email, to = 'INOKS Ödeme Yapıldı', 'ik@oxityazilim.com', payment.profile.user.email
            text_content = 'Sayın ' + payment.profile.user.first_name + ' ' + payment.profile.user.last_name + '<br>'
            html_content = payment.payedDate + ' dönemine ait' + payment.paymentTotal + ' ₺ ödemeiniz yapılmıştır.'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
