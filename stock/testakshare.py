import akshare as ak
import pandas as pd
import sqlite3
import re
import tushare as ts
token='dbc18146da72de099f72be761b74fcfd3b4b9d45c17eda93a8b89266'    #（注册后生成）
ts.set_token(token)
pro=ts.pro_api()
# from stock.myinform import StockTrade,StockInform
from stock import myinform
import qstock as qs
import datetime

sql3 = sqlite3.connect("test.db")

def main():
    """Run administrative tasks."""
    # northdata()
    # sql3 = sqlite3.connect("northcapital.db")
    code='001286'
    # dic = value_of_future(code)
    # print(dic)
    # print(dic['code'])
    price = 13.32
    quantity = 500
    flag = 'sell'
    # cal_fee(code=code, price=price, quantity=quantity, flag=flag)
    stock = myinform.StockInform(symbol=code)
    print(stock.name,stock.location,stock.category)

    buystock = myinform.StockTrade(symbol=code,quantity=quantity,price=price,mark=flag)
    print(buystock.location)
    print(buystock.ammount,buystock.commission,buystock.tranfer_fee,buystock.stamp_tax,buystock.stock_cost)
    print(get_index_ascent())

    # stock_yjbb_em_df = ak.stock_yjbb_em(date="20221231")
    # # stock_yjbb_em_df =  stock_yjbb_em_df.drop(labels=['最新公告日期','所处行业'],axis=1)
    # #
    # # print(stock_yjbb_em_df)
    # # stock_roe2022over15 = stock_yjbb_em_df[stock_yjbb_em_df.净资产收益率>15]
    # # print(stock_roe2022over15)
    #
    # col_n = ['股票代码','股票简称','净资产收益率']
    # df1 = pd.DataFrame(stock_yjbb_em_df,columns=col_n)
    # print(df1)
    # stock_roe2022over15 = df1[df1.净资产收益率 > 15]
    # stock_roe2022over15.rename(columns={'净资产收益率': 'ROE2022'}, inplace=True)
    # print(stock_roe2022over15)
    roe_2022 = getroe('20221231')
    print(roe_2022)
    roe_2021 = getroe('20211231')
    print(roe_2021)
    roe_2020 = getroe('20201231')
    roe_2019 = getroe('20191231')
    roe_2018 = getroe('20181231')
    roe = pd.merge( roe_2018,roe_2019,how='outer')
    roe = pd.merge(roe,roe_2020,how='outer')
    roe = pd.merge(roe,roe_2021,how='outer')
    roe = pd.merge(roe,roe_2022,how='outer')
    roe = roe.dropna(axis='rows')
    print(roe)




def northdata():
    stock_em_hsgt_hold_stock_df = ak.stock_hsgt_hold_stock_em(market="北向", indicator="今日排行")
    print(stock_em_hsgt_hold_stock_df.info())



def getlatestprice(code):
    stockdata = ak.stock_zh_a_spot_em()
    index = stockdata[(stockdata.代码==code) ].index.tolist()
    price = stockdata.iloc[index]['最新价']
    return float(price)

def getstockname (code):
    stockinfo = ak.stock_individual_info_em(symbol=code)
    value = stockinfo['value']
    name = value[5]
    return name

# newprice  = getlatestprice(code)
# print (newprice)
# name = getstockname(code)
# print (name)

def getpricelist(codelist):
    code = '600036'
    stockdata = ak.stock_zh_a_spot_em()
    price_list = []
    for i in codelist:
        index = stockdata[(stockdata.代码 == code)].index.tolist()
        price = stockdata.iloc[index]['最新价']
        price_list.append(float(price))
    return price_list


def calPEG():
 # 根据每股收益的预测值计算出GRR(增长率），再根据市盈率计算PEG
 # 盈利预测 通过 接口 ak.stock_profit_forecast()，市盈率 通过 ak.stock_zh_a_spot_em()
    stockdata = ak.stock_zh_a_spot_em()
    reportquanity = 10
    stock_profit_forecast_df = ak.stock_profit_forecast_em(symbol="")
    # print(stock_profit_forecast_df)
    # print(type(stock_profit_forecast_df))
    reportoverten_df = stock_profit_forecast_df[stock_profit_forecast_df.研报数 > reportquanity]
    # print(reportoverten_df)
    reportoverten_df.insert(loc=13, column='GRR', value=0)
    reportoverten_df.insert(loc=14, column='PE ttm', value=0)
    reportoverten_df.insert(loc=15, column='PEG', value=0)
    # print(reportoverten_df)
    dflen_int = len(reportoverten_df)
    for i in range(dflen_int):
        # if reportoverten_df.iloc[i, 9] < 0:
        #     reportoverten_df.iloc[i, 13] = -1
        # else:
        #     reportoverten_df.iloc[i, 13] = (pow((reportoverten_df.iloc[i, 12] / reportoverten_df.iloc[i, 9]),
        #                                        1 / 3) - 1)*100  # 计算PEG
        code = reportoverten_df.iloc[i, 1]
        close = getlatestprice(code)
        growth_n2_n1 = (reportoverten_df.iloc[i, 12]-reportoverten_df.iloc[i, 11])/reportoverten_df.iloc[i, 11]
        pe_n2 = close/reportoverten_df.iloc[i, 12]
        # reportoverten_df.iloc[i, 13] = growth_n2_n1
        index = stockdata.loc[stockdata.代码 == code].index.tolist()[0]
        reportoverten_df.iloc[i, 13] = growth_n2_n1
        # reportoverten_df.iloc[i, 14] = stockdata.iloc[index, 15]
        reportoverten_df.iloc[i, 14] = pe_n2
        reportoverten_df.iloc[i, 15] = reportoverten_df.iloc[i, 14] / (reportoverten_df.iloc[i, 13] )
        # list_code.append(reportoverten_df.iloc[i,1])
    # print(reportoverten_df)

    # 设置筛选条件 0<PEG<1 GRR<40%
    reportoverten_df = reportoverten_df[reportoverten_df.PEG > 0]
    reportoverten_df = reportoverten_df[reportoverten_df.GRR < 40 ]
    select_peg = reportoverten_df[reportoverten_df.PEG < 1 ].sort_values(by='PEG', ascending=True)
    # print(select_peg)
    # html_text = select_peg.to_html()
    # print(html_text)
    # select_peg = select_peg.drop(select_peg.columns[4],axis=1)
    return select_peg



def value_of_future(code):
    close = getlatestprice(code)
    name = getstockname(code)
    fore_eps_df =  ak.stock_profit_forecast_ths(symbol=code, indicator="预测年报每股收益")   #获取预估盈利
    # print(close)
    # print(name)
    # print(fore_eps_df)
    fore_eps_list = []
    for i in range(3):
        fore_eps_list.append(fore_eps_df.iloc[i,3])   # 将预估每股收益放在数组中
    # print(fore_eps_list)
    price_evaluate = fore_eps_list[2]*(fore_eps_list[2]/fore_eps_list[1]-1)*100    #预估2年后的估值
    price_evaluate = "%.2f" % (price_evaluate)     #只保留2位小小数
    # print(price_evaluate)
    voa_dic = {'code':code,
               'name':name,
               'close':close,
                'epsn':fore_eps_list[0],
               'epsn1':fore_eps_list[1],
               'epsn2':fore_eps_list[2],
                'voa':price_evaluate,
               'voa_pre':0,
               }       #将所有数据打包在字典中,便于返回
    # print(voa_dic)
    return voa_dic


def cal_fee(code,price,quantity,flag):
    print('you are kind')
    guohufei_ratio = 0.01/1000
    yinhuatax_ratio = 1/1000
    yongjin_ratio = 1.313/10000
    zhengguanfei_ratio = 0.002/100
    jingshoufei_ratio = 0.0487/1000
    jngshoufei_fund_sh_ratio = 0.045 / 1000


    basic_fee = price * quantity

    if code[0]=='6':
        yongjin = basic_fee * yongjin_ratio
        if yongjin <= 5:
            yongjin = 5
        if flag == 'B':
            total =  basic_fee *(1 + guohufei_ratio + zhengguanfei_ratio + jingshoufei_ratio) + yongjin
        elif flag == 'S':
            total = basic_fee *(1 - guohufei_ratio - zhengguanfei_ratio - jingshoufei_ratio - yinhuatax_ratio) - yongjin
    if code[0] =='5':
        print('上海 ETF')
    if code[0] == '0' or code[0] == '3' or code[0] ==3:
        yinhuatax = basic_fee * yinhuatax_ratio
        if yongjin <= 5:
            yongjin = 5
        if flag == 'B':
            total =  basic_fee *(1 + zhengguanfei_ratio + jingshoufei_ratio) + yongjin
        elif flag == 'S':
            total = basic_fee * (1 - zhengguanfei_ratio - jingshoufei_ratio - yinhuatax_ratio) - yongjin
    if code[0] == '1':
        print('深圳 ETF')
    # print(guohufei)
    print(yongjin)
    # print(yinhuatax)
    print(total)





def get_index_ascent():
    # ascent = {}
    codelist = ['510050','159915']

    # print(b[-1])
    # print(b[-20:-1])
    # print(b[-20])
    # today = datetime.datetime.today().strftime('%Y%m%d')
    deltatime = datetime.timedelta(days =40)
    foreday = (datetime.datetime.today()-deltatime).strftime('%Y%m%d')
    # print(today)
    print(foreday)
    # ratio = (b[-1]-b[-20])/b[-20]
    # print(ratio)
    df = qs.get_data(codelist,start=foreday)
    a = df.iloc[0]
    df_sz = df[df['code']=='510050']
    sz_close_list= df_sz['close'].values
    sz_ratio = (sz_close_list[-1]-sz_close_list[-20])/sz_close_list[-20]

    df_cyb =   df[df['code']=='159915']
    cyb_close_list = df_cyb['close'].values
    cyb_ratio = (cyb_close_list[-1]-cyb_close_list[-20])/cyb_close_list[-20]

    ascent={'sz_ratio':round(sz_ratio,3), 'cyb_ratio':round(cyb_ratio,3)}
    return ascent

    # print(df)
    # print(a)
    # print(b)
    #
    #

def getroe(date):
    stock_yjbb_em_df = ak.stock_yjbb_em(date=date)
    # stock_yjbb_em_df =  stock_yjbb_em_df.drop(labels=['最新公告日期','所处行业'],axis=1)
    #
    # print(stock_yjbb_em_df)
    # stock_roe2022over15 = stock_yjbb_em_df[stock_yjbb_em_df.净资产收益率>15]
    # print(stock_roe2022over15)

    col_n = ['股票代码','股票简称','净资产收益率']
    df1 = pd.DataFrame(stock_yjbb_em_df,columns=col_n)
    # print(df1)
    year = date[0:4]
    print(year)
    col_name = 'ROE'+year
    stock_roeover15 = df1[df1.净资产收益率 > 15]
    stock_roeover15.rename(columns={'净资产收益率': col_name}, inplace=True)
    # print(stock_roe2022over15)
    return stock_roeover15


if __name__ == '__main__':
    main()