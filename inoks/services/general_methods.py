import calendar
import datetime

import pytz
from django.contrib.auth.models import User, Permission
from django.db.models import Sum
from django.http import JsonResponse

from inoks.models import Profile, Order, Menu, MenuAdmin, Refund, earningPayments, OrderSituations, ProductCategory, \
    Settings, Product
from inoks.models.Address import Address
from inoks.models.Coupon import Coupon

from inoks.models.ProfileControlObject import ProfileControlObject
from inoks.models.UserProductObject import UserProductObject


def getMenu(request):
    menus = Menu.objects.all().order_by('name')

    return {'menus': menus}


def options(request):
    option = Settings.objects.get(name='kdv')
    options_dict = dict()
    options_dict['tax'] = option.value

    return {'options_dict': options_dict}


def getAdminMenu(request):
    adminmenus = MenuAdmin.objects.all().order_by('name')
    return {'adminmenus': adminmenus}


def get_category_home(request):
    categories = ProductCategory.objects.all()

    return {'categories': categories}


def activeUser(request, pk):
    user = Profile.objects.get(pk=pk)
    user.isApprove = True
    user.activePassiveDate = datetime.datetime.now()
    user.user.is_active = True
    user.isActive = True
    user.save()
    user.user.save()
    return user


def passiveUser(request, pk):
    user = Profile.objects.get(pk=pk)
    user.user.is_active = False
    user.isActive = False
    user.isApprove = False
    user.activePassiveDate = datetime.datetime.now()
    user.save()
    user.user.save()
    return user


def reactiveUser(request, pk):
    user = Profile.objects.get(pk=pk)
    user.user.is_active = True
    user.isActive = True
    user.isApprove = True
    user.save()
    user.user.save()
    return user


def activeOrder(request, pk):
    order = Order.objects.get(pk=pk)
    order.order_situations.add(OrderSituations.objects.get(name="Hazırlanıyor"))
    order.isApprove = True
    order.save()
    return order


def activeRefund(request, pk):
    refund = Refund.objects.get(pk=pk)
    refund.isApprove = True
    refund.save()
    return refund


def passiveRefund(request, pk):
    refund = Refund.objects.get(pk=pk)
    refund.isApprove = False
    refund.save()
    return refund


def existMail(mail):
    users = User.objects.filter(email=mail)
    if len(users) == 0:
        return False
    else:
        return True


# sponsor sponsor  olanları getir
def rtrnProfileBySponsorID(profile_list):
    # profiles = Profile.objects.filter(sponsor=sponsor)

    copy_profile_list = profile_list.copy()

    for prof in copy_profile_list:

        if not prof.is_controlled:
            profiles = Profile.objects.filter(sponsor=prof.profile)
            for profile in profiles:
                # total_order = monthlyMemberOrderTotal(profile)['total_price']
                total_order = MemberAllOrderTotal(profile)['total_price']
                if total_order is None:
                    total_order = 0
                total_order = str(float(str(total_order).replace(",", ".")))

                profile_object = ProfileControlObject(profile=profile, is_controlled=False,
                                                      total_order=total_order)
                profile_list.append(profile_object)

            for index in range(len(profile_list)):
                if profile_list[index] == prof:
                    profile_list[index].is_controlled = True

    res = sum(1 for i in profile_list if not i.is_controlled)

    if res == 0:
        return profile_list

    return rtrnProfileBySponsorID(profile_list)


def monthlyMemberOrderTotal(profile):
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]
    order2 = Order.objects.filter(creationDate__range=(datetime_start, datetime_end)).filter(
        profile=profile)
    orders_sum = Order.objects.filter(creationDate__range=(datetime_start, datetime_end)).filter(isApprove=True).filter(
        profile=profile).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum


def MemberAllOrderTotal(profile):
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]
    order2 = Order.objects.filter(
        profile=profile)
    orders_sum = Order.objects.filter(isApprove=True).filter(
        profile=profile).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum


def monthlyMemberOrderTotalByDate(profile, month, year):
    datetime_current = datetime.datetime.today()
    year = year
    month = month
    num_days = calendar.monthrange(year, month)[1]

    datetime_start = datetime.datetime(year, month, 1, 0, 0)

    datetime_end = datetime.datetime(year, month, num_days, 23, 59)

    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]
    order2 = Order.objects.filter(creationDate__range=(datetime_start, datetime_end)).filter(isApprove=True).filter(
        profile=profile)
    orders_sum = Order.objects.filter(creationDate__range=(datetime_start, datetime_end)).filter(isApprove=True).filter(
        profile=profile).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum


def returnLevelTreeByDate(profileArray, levelDict, level, month, year):
    profiles = []
    profiles = Profile.objects.filter(id__in=profileArray)
    profile_list = []

    for profile in profiles:
        total_order = monthlyMemberOrderTotalByDate(profile, month, year)['total_price']
        if total_order is None:
            total_order = 0
        total_order = str(float(str(total_order).replace(",", ".")))

        profile_object = ProfileControlObject(profile=profile, is_controlled=False,
                                              total_order=total_order)
        profile_list.append(profile_object)

    levelDict[str(level)] = profile_list

    id_array = []

    if level < 7:
        for profile in profiles:

            profileSponsor = Profile.objects.filter(sponsor__id=profile.id)

            for sponsor in profileSponsor:
                id_array.append(sponsor.id)

        returnLevelTreeByDate(id_array, levelDict, level + 1, month, year)

    elif level == 7:
        return levelDict

    else:
        return 0


def returnLevelTree(profileArray, levelDict, level):
    profiles = []
    profiles = Profile.objects.filter(id__in=profileArray)
    profile_list = []

    for profile in profiles:
        total_order = monthlyMemberOrderTotal(profile)['total_price']
        if total_order is None:
            total_order = 0
        total_order = str(float(str(total_order).replace(",", ".")))

        profile_object = ProfileControlObject(profile=profile, is_controlled=False,
                                              total_order=total_order)
        profile_list.append(profile_object)

    levelDict[str(level)] = profile_list

    id_array = []

    if level < 7:
        for profile in profiles:

            profileSponsor = Profile.objects.filter(sponsor__id=profile.id)

            for sponsor in profileSponsor:
                id_array.append(sponsor.id)

        returnLevelTree(id_array, levelDict, level + 1)

    elif level == 7:
        return levelDict

    else:
        return 0


def calculate_earning(levelDict, level):
    earning = 0

    if level == 1:
        print(levelDict[str(level)])
        return 0

    if level == 2:
        if len(levelDict[str(level)]) == 3:

            for orderPrice in levelDict[str(level)]:
                earning = earning + float(orderPrice.total_order)

            if earning < 2500:
                return 0
            else:
                return float(earning * 6 / 100)

    if level == 3:
        if len(levelDict[str(level)]) == 9:
            for orderPrice in levelDict[str(level)]:
                earning = earning + float(orderPrice.total_order)

            if earning < 7500:
                return 0
            else:
                return float(earning * 5 / 100)

    if level == 4:

        for orderPrice in levelDict[str(level)]:
            earning = earning + float(orderPrice.total_order)

        if earning < 22500:
            return 0
        else:
            return float(earning * 4 / 100)

    if level == 5:

        for orderPrice in levelDict[str(level)]:
            earning = earning + float(orderPrice.total_order)

        if earning < 67500:
            return 0
        else:
            return float(earning * 3 / 100)

    if level == 6:

        for orderPrice in levelDict[str(level)]:
            earning = earning + float(orderPrice.total_order)

        if earning < 202500:
            return 0
        else:
            return float(earning * 2 / 100)

    if level == 7:

        for orderPrice in levelDict[str(level)]:
            earning = earning + float(orderPrice.total_order)

        if earning < 607500:
            return 0
        else:
            return float(earning * 1 / 100)
    return 0


def calculate_order_of_tree(levelDict):
    earning = 0

    for i in range(7):

        if i + 1 == 1:
            for orderPrice in levelDict[str(i + 1)]:
                earning = earning + float(orderPrice.total_order)

        if i + 1 == 2:

            for orderPrice in levelDict[str(i + 1)]:
                earning = earning + float(orderPrice.total_order)

        if i + 1 == 3:

            for orderPrice in levelDict[str(i + 1)]:
                earning = earning + float(orderPrice.total_order)

        if i + 1 == 4:

            for orderPrice in levelDict[str(i + 1)]:
                earning = earning + float(orderPrice.total_order)

        if i + 1 == 5:

            for orderPrice in levelDict[str(i + 1)]:
                earning = earning + float(orderPrice.total_order)

        if i + 1 == 6:

            for orderPrice in levelDict[str(i + 1)]:
                earning = earning + float(orderPrice.total_order)

        if i + 1 == 7:

            for orderPrice in levelDict[str(i + 1)]:
                earning = earning + float(orderPrice.total_order)

    return earning


def calculate_earning_of_tree(levelDict, total_order_member):
    earning = 0

    kademe = 0

    total_order = calculate_order_of_tree(levelDict)

    total_order_member = total_order_member['total_price']

    if total_order_member is None:
        total_order_member = 0

    total_order1 = (total_order * 100) / 118

    if total_order >= 10648000:
        earning = float(total_order1 * 1 / 100)
        kademe = 10

    elif 4840000 <= total_order < 10648000:
        earning = float(total_order1 * 2 / 100)
        kademe = 9

    elif 2200000 <= total_order < 4840000:
        earning = float(total_order1 * 3 / 100)
        kademe = 8

    elif 1000000 <= total_order < 2200000:
        earning = float(total_order1 * 4 / 100)
        kademe = 7

    elif 607500 <= total_order < 1000000:
        earning = float(total_order1 * 1 / 100)
        kademe = 6

    elif 202500 <= total_order < 607500:
        earning = float(total_order1 * 2 / 100)
        kademe = 5

    elif 67500 <= total_order < 202500:
        earning = float(total_order1 * 3 / 100)
        kademe = 4

    elif 22500 <= total_order < 67500:
        earning = float(total_order1 * 4 / 100)
        kademe = 3

    elif 7500 <= total_order < 22500:
        if len(levelDict[str(3)]) == 9:
            earning = float(total_order1 * 5 / 100)
            kademe = 2
        elif len(levelDict[str(2)]) == 3:
            earning = float(total_order1 * 6 / 100)
            kademe = 1
        else:
            earning = 0

    elif 2500 <= total_order < 22500:
        if len(levelDict[str(2)]) == 3:
            earning = float(total_order1 * 6 / 100)
            kademe = 1
        else:
            earning = 0

    else:
        earning = 0

    # kademeye göre sipariş kontrolü
    if kademe == 0:
        earning = 0

    elif kademe == 1:
        if total_order_member >= 60:
            earning = earning
        else:
            earning = 0

    elif kademe == 2:
        if total_order_member >= 60:
            earning = earning
        else:
            earning = 0

    elif kademe == 3:
        if total_order_member >= 60:
            earning = earning
        else:
            earning = 0

    elif kademe == 4:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 5:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 6:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 7:
        if total_order_member >= 240:
            earning = earning
        else:
            earning = 0

    elif kademe == 8:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 9:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    elif kademe == 10:
        if total_order_member >= 120:
            earning = earning
        else:
            earning = 0

    else:
        earning = 0

    return earning


def monthlyTotalPaidByDate(month, year):
    orders_sum = earningPayments.objects.filter(payedDate=month + '/' + year)

    total = 0

    for totals in orders_sum:
        total = float(total) + float(totals.paymentTotal)

    return total


def monthlOrderTotalAllTime():
    # scores = Score.objects.filter(creationDate__range=(datetime_start, datetime_end)).order_by('score')[:100]

    orders_sum = Order.objects.filter(isApprove=True).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum['total_price']


def monthlMemberOrderTotalAllTime(profile):
    orders_sum = Order.objects.filter(isApprove=True).filter(
        profile=profile).aggregate(
        total_price=Sum('totalPrice'))

    return orders_sum


def show_urls(urllist, depth=0):
    urls = []

    # show_urls(urls.urlpatterns)
    for entry in urllist:

        urls.append(entry)
        perm = Permission(name=entry.name, codename=entry.pattern.regex.pattern, content_type_id=11)

        if Permission.objects.filter(name=entry.name).count() == 0:
            perm.save()
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

    return urls


def control_access(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin":
        is_exist = True

    return is_exist


def couponControl(coupon_code, total_order):
    discount = 0
    message = ""
    type = ""
    try:

        coupon = Coupon.objects.filter(code=coupon_code)
        now = datetime.datetime.now()
        now = pytz.utc.localize(now)
        if len(coupon) > 0:
            coupon = coupon[0]
            if coupon.isActive and coupon.stock > 0 and coupon.finishDate > now:
                if coupon.isLimit and coupon.limit <= float(total_order):
                    discount = coupon.discount

                elif not coupon.isLimit:
                    discount = coupon.discount

                else:
                    discount = 0

                return discount

        else:
            return discount

    except Exception as e:

        return discount


def products_in_card(cards):
    orders = []
    for product in cards:
        order = UserProductObject(id=0, product_name=None, price=0, count=0, image=None, subtotal=0, slug=None)
        order.id = product['id']
        order.product_name = product['name']
        order.price = product['price']
        order.count = product['count']
        order.subtotal = product['count'] * product['price']
        orders.append(order)


    return orders



