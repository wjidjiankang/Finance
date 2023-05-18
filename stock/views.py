from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.shortcuts import
# from django.shortcuts import
from stock import models
from stock import forms
import akshare as ak
from stock import  testakshare
import pandas as pd
import qstock as qs
from stock import myinform

# Create your views here.





def getsymbol(code):
    if len(code) == 6:
        if code[0] == '6':
            codeforname = code+'.SH'
        elif code[0] == '0' or code[0] == '3':
            codeforname =code + '.SZ'
    return codeforname


def getpricelist(codelist):
    """
    通过股票代码 获取股票的当前价格，涨幅，前日收盘价格
    """
    # stockdata = ak.stock_zh_a_spot_em()
    # price_list = []
    # for i in codelist:
    #     li = []
    #     index = stockdata[(stockdata.代码 == i)].index.tolist()
    #     price = stockdata.iloc[index]['最新价']
    #     print(price)
    #
    #     ratio = stockdata.iloc[index]['涨跌幅']
    #     preclose = stockdata.iloc[index]['昨收']
    #     print(preclose)
    #     li.append(float(price))
    #     li.append(ratio)
    #     li.append(float(preclose))
    #
    #     price_list.append(li)
    # return price_list
    # 使用qstock库重新写了
    stockdata  = qs.realtime_data(code=codelist)
    # print(df)
    price_list =[]
    for i in range(len(codelist)):
        li = []
        price = stockdata.iloc[i]['最新']
        ratio = stockdata.iloc[i]['涨幅']
        preclose = stockdata.iloc[i]['昨收']
        li.append(float(price))
        li.append(ratio)
        li.append(float(preclose))
        price_list.append(li)
    # print(price_list)
    return price_list



def getstockname (code):
    # stockinfo = ak.stock_individual_info_em(symbol=code)
    '''
    使用qstock库重新写了
    '''
    stockinfo = qs.realtime_data(code=code )
    # value = stockinfo['value']
    # name = value[5]
    name = stockinfo['名称'][0]
    return name



def index(request):
    return render(request, "index.html")


def loginz(request):
    return render(request,'loginz.html')

def data_entry(request):
    # user_list_obj = models.Fund.objects.order_by("-id")
    list_obj = models.Stock.objects.order_by("id").reverse()
    user_list_obj = list_obj[:30]
    # funds = user_list_obj
    # print(funds,type(funds))
    #return render(request, 't1.html', {'li': user_list_obj})
    return render(request,'data_entry.html',{'li': user_list_obj})



def buystock(request):
    bstock = models.Stock()
    mystock = models.StockInHand()
    # mystock_profit = models.StockProfitbyOp()
    if request.method == 'POST':
        mark = 'Buy'
        code = request.POST.get('bcode')
        # name = getname(code)
        # name = getstockname(code)
        quantity = float(request.POST.get('bquantity'))
        # amount = request.POST.get('bamount')
        price = float(request.POST.get('bprice'))
        # name = '比亚迪'
        buystock = myinform.StockTrade(symbol=code, quantity=quantity, mark=mark, price=price)
        bstock.code = buystock.code
        bstock.name = buystock.name
        bstock.quantity = buystock.quantity
        bstock.amount = buystock.ammount
        bstock.mark = mark
        bstock.price = price
        bstock.save()

    stocks  = models.StockInHand.objects.filter(code =code)
    word = "买入成功"
    if stocks :
        mystock = stocks[0]
        mystock.quantity = mystock.quantity+ bstock.quantity
        mystock.amount = float(mystock.amount) + bstock.amount
    else:
        mystock.code = buystock.code
        mystock.name = buystock.name
        mystock.quantity = bstock.quantity
        mystock.amount = bstock.amount
        mystock.ratio = 0
    mystock.cost = mystock.amount / mystock.quantity
    mystock.save()
    # print (mystock.amount)

    # stocks_profit = models.StockProfitbyOp.objects.filter(code =code)
    # if stocks_profit :
    #     mystock_profit = stocks_profit[0]
    #     mystock_profit.cost = (float(mystock_profit.cost)*float(mystock_profit.ttlquantity) + float(amount))/(float(mystock_profit.ttlquantity)+float(quantity))
    #     mystock_profit.ttlquantity = float(mystock_profit.ttlquantity)+float(quantity)
    # else:
    #     mystock_profit.code  = code
    #     mystock_profit.name = name
    #     mystock_profit.ttlquantity = bstock.quantity
    #     mystock_profit.cost = float(amount)/float(bstock.quantity)
    # mystock_profit.save()

    list_obj = models.Stock.objects.order_by("id").reverse()
    user_list_obj = list_obj[:20]
    # user_list_obj = models.Fund.objects.filter(name ='比亚迪')
    # user_list_obj = models.Fund.objects.last()
    return render(request, 'data_entry.html', {'li': user_list_obj,'word':word})


def showstock(request):
    stocks = models.StockInHand.objects.exclude(quantity = 0)
    totalvalue = 0
    totalprofit = 0
    total_day_profit = 0

    for stock in stocks:
        moreinform = myinform.BasicInform(stock.code)
        stock.price = moreinform.latestprice
        stock.value = stock.quantity * stock.price
        stock.profit = stock.value - float(stock.amount)
        stock.ratio = moreinform.ratio
        stock.profit_today = float((moreinform.latestprice - moreinform.preclose)) * stock.quantity
        stock.save()
        totalvalue = stock.quantity * stock.price + totalvalue
        totalvalue = round(totalvalue, 2)
        totalprofit = totalprofit + stock.profit
        total_day_profit = total_day_profit + stock.profit_today
    for stock in stocks:
        proportion = (float(stock.price) * float(stock.quantity)*100)/totalvalue
        stock.value_proportion = proportion
        stock.save()
    totalprofit = format(totalprofit,'.2f')
    total_day_profit = format(total_day_profit,'.2f')
    user_list_obj = models.StockInHand.objects.exclude(quantity = 0).order_by('ratio').reverse()
    # stock_list = models.StockInHand.objects.order_by('profit').reverse()
    # stock_list_profit = models.StockProfitbyOp.objects.all()
    return render(request, 'showstock.html', {'li': user_list_obj,'totalcost':totalvalue,'totaltoday':total_day_profit,'totalprofit':totalprofit})


def sellstock(request):
    sstock = models.Stock()
    mystock = models.StockInHand()
    # stockprofit = models.StockProfitbyOp()
    if request.method == 'POST':
        mark = 'Sell'
        code = request.POST.get('scode')

        # name = getname(code)
        # name = getstockname(code)
        # name = stockinhand.name
        quantity = float(request.POST.get('squantity'))
        # amount = request.POST.get('samount')
        price = float(request.POST.get('sprice'))
        sell_stock = myinform.StockTrade(symbol=code, quantity=quantity, mark=mark,price=price)
        stockinhand = models.StockInHand.objects.get(code=sell_stock.code)
        # name = '比亚迪'
        # stockinhand = models.StockInHand.objects.get(code=code)

        sstock.code = sell_stock.code
        sstock.name = sell_stock.name
        sstock.quantity =0.0- quantity
        sstock.amount = 0.0-sell_stock.ammount
        sstock.mark = mark
        sstock.price = price
        sstock.save()

        # stockprofit.code = code
        # stockprofit.name = name
        # stockprofit.quantity = float(quantity)
        # # stockprofit.cost = float(stockinhand.cost)
        # stockprofit.profit = float(amount)-float(quantity) * float(stockinhand.cost)
        # stockprofit.save()

    # stocks = models.StockInHand.objects.get(code=code)
    word = "卖出成功"
    if stockinhand:
        # mystock = stocks[0]
        sstock.sell_profit = (float(sstock.price) -(float(stockinhand.amount)/float(stockinhand.quantity)))*sell_stock.quantity
        stockinhand.quantity = stockinhand.quantity + sstock.quantity
        stockinhand.amount = float(stockinhand.amount) + sstock.amount
        sstock.save()
        if stockinhand.quantity == 0:
            stockinhand.cost = 0
        else:
            stockinhand.cost = stockinhand.amount /stockinhand.quantity

        # print(stockinhand.amount)
    # else:
    #     mystock.code = code
    #     mystock.name = name
    #     mystock.quantity = bstock.quantity
    #     mystock.amount = bstock.amount
    # mystock.cost = mystock.amount / mystock.quantity
    stockinhand.save()

    list_obj = models.Stock.objects.order_by("id").reverse()
    user_list_obj = list_obj[:30]
    # user_list_obj = models.Fund.objects.filter(name ='比亚迪')
    # user_list_obj = models.Fund.objects.last()
    return render(request, 'data_entry.html', {'li': user_list_obj, 'word': word})
    # return render(request, "showstock.html")


def caldcf(request):
    return render(request,'caldcf.html')

def cal_dcf(request):
    if request.method == 'POST':
        # a= request.POST.get('base_dcf')
        # print (a)
        try:
            base_dcf = float(request.POST.get('base_dcf'))
            discountratio = float(request.POST.get('discountratio'))
        except:
            base_dcf = 0
            discountratio = 10

        try:
            ratio1 = float(request.POST.get('ratio1'))
            year1 = float(request.POST.get('year1'))
        except:
            ratio1 = 0
            year1 = 0
        factorq1 = (1+ratio1/100)/(1+discountratio/100)
        head1 = base_dcf * factorq1
        subttl1 = head1*(1-pow(factorq1,year1))/(1-factorq1)

        try:
            ratio2 = float(request.POST.get('ratio2'))
            year2 = float(request.POST.get('year2'))
        except:
            ratio2 = 0
            year2 = 0
        factorq2 = (1 + ratio2 / 100) / (1 + discountratio / 100)
        base1  = base_dcf * pow(factorq1,year1)
        head2 = base1 * factorq2
        # print(base_dcf * pow(factorq1,year1))
        # print(head2)
        subttl2 = head2 * (1 - pow(factorq2, year2)) / (1 - factorq2)

        try:
            ratio3 = float(request.POST.get('ratio3'))
            year3 = float(request.POST.get('year3'))
        except:
            ratio3 = 0
            year3 = 0
        factorq3 = (1 + ratio3 / 100) / (1 + discountratio / 100)
        base2 = base1*pow(factorq2,year2)
        head3 = base2* factorq3
        subttl3 = head3 * (1 - pow(factorq3, year3)) / (1 - factorq3)

        try:
            ratio4 = float(request.POST.get('ratio4'))
            year4 = float(request.POST.get('year4'))
        except:
            ratio4 = 0
            year4 = 0
        factorq4 = (1 + ratio4 / 100) / (1 + discountratio / 100)
        base3= base2*pow(factorq3,year3)
        head4 = base3 * pow(factorq3, year3) * factorq4
        subttl4 = head4 * (1 - pow(factorq4, year4)) / (1 - factorq4)

        total = subttl1 +subttl2 + subttl3 + subttl4
        try :
            totalstock = float(request.POST.get('totalstock'))
            price  = total/totalstock
        except:
            totalstock = -1
            price  = "请输入正确的数字"
    return render(request,'caldcf.html',{'subttl1':subttl1,'subttl2':subttl2,'subttl3':subttl3,'subttl4':subttl4,'total':total,'price':price})



def getword(request):

    if request.method !='POST':
        form = forms.GetwordForm()
    else:
        form = forms.GetwordForm(data = request.POST)
        if form.is_valid():
            form.save()
            # new_entry = form.save(commit=False)
            # new_entry.save()
            return HttpResponseRedirect(reverse('stock:getword'))
    context={'form':form}
    return render(request,'getword.html',context)



# def showpeg(request):
#     # peg_boj = models.PEGData()
#     df = testakshare.calPEG()
#     models.PEGData.objects.all().delete()
#     # print(df[1][1])
#     len_int = len(df)
#     insert_list = []
#     # 通过bulk_create的方法批量存储到数据库
#     for i in range(len_int):
#             insert_list.append(models.PEGData(code=df.iloc[i][1], name=df.iloc[i][2],reportqty = df.iloc[i][3],GRR = df.iloc[i][13],PEttm = df.iloc[i][14],PEG = df.iloc[i][15],profit_n = df.iloc[i][9],profit_n1 = df.iloc[i][10],profit_n2 = df.iloc[i][11],profit_n3 = df.iloc[i][12]))
#     models.PEGData.objects.bulk_create(insert_list)
#
#     # print(peg_boj)
#     # peg_boj.save()
#     li_obj = models.PEGData.objects.all()
#     return render(request, 'showpeg.html', {'li': li_obj}, )

# def test(request):
#     teststring = 'I am man'
#     # print(teststring)
#     # for item in teststring:
#     #     print (item)
#     data = {'name': ['apple', 'egg', 'watermelon'], 'color': ['red', 'yellow', 'green'], 'num': [30, 40, 50]}
#     df1 = pd.DataFrame(data)
#     print (df1)
#     items = df1.itertuples()
#     myfruit = models.Fruit()
#     n = 10
#     for item in teststring:
#         # print (item[1])
#
#         # myfruit.color = item[2]
#         models.Fruit.objects.create(name = item,quantity = n)
#         n = n+1
#
#     return render(request,'test.html',{'li':teststring},)


def predict(request):
    price_predict = models.ValueOfAssenment()
    data_dic={}
    if request.method == 'POST':
        symbol  = request.POST.get('code')
        try:
            predict_stock = myinform.PredictValue(symbol)
            stocks = models.ValueOfAssenment.objects.filter(code=predict_stock.code)
            print(stocks)
            n=len(stocks)
            print(n)
            if n >= 1:
                stock = stocks[n-1]
                voa_pre = stock.voa
            else:
                voa_pre = 0
            price_predict.code = predict_stock.code
            price_predict.name = predict_stock.name
            price_predict.close = predict_stock.latestprice
            price_predict.eps_n = predict_stock.epsn
            price_predict.eps_n1 = predict_stock.epsn1
            price_predict.eps_n2 = predict_stock.epsn2
            price_predict.voa = predict_stock.voa
            price_predict.save()
            data_dic = {'code': predict_stock.code,
                        'name': predict_stock.name,
                        'close': predict_stock.latestprice,
                        'epsn': predict_stock.epsn,
                        'epsn1': predict_stock.epsn1,
                        'epsn2': predict_stock.epsn2,
                        'voa': predict_stock.voa,
                        'voa_pre': voa_pre,
                        }
        except:
            data_dic = {'code': symbol,
                        'name': symbol,
                        'voa':'出错了！',}
    print(data_dic)
    return render(request,'predict.html',data_dic)

def stock_clearance(request):
    stocks  = models.StockInHand.objects.filter(quantity=0).order_by('-profit')
    total_profit = 0
    for stock in stocks:
        total_profit = stock.profit + total_profit
    return render(request, 'stock_clearance.html', {'stocks':stocks,'totalprofit':total_profit})




