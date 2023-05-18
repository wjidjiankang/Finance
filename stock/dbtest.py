from django.shortcuts import render,redirect,HttpResponse
# from django.shortcuts import
# from django.shortcuts import
from stock import models
# from stock.models  import Stock


def dbaseTest(request):
    # myfund = models.Fund()
    # code = '620012'
    # name = "中国平安"
    # mark = 'B'
    # qty = 500
    # amt = 15402
    #
    # myfund.code = code
    # myfund.name = name
    # myfund.mark = mark
    # myfund.qty = qty
    # myfund.amt = amt
    #
    # print(myfund.qty)
    myfund = models.Fund(code="300126",name ="中华只要",mark="B",qty= 200, amt = 4000)
    # book.save()
    myfund.save()
    user_list_obj = models.Fund.objects.all()
    return render(request, 't2.html', {'list': user_list_obj})