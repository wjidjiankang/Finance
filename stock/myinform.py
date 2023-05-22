import akshare as ak
import pandas as pd
import sqlite3
import re
import tushare as ts
import qstock as qs

token='dbc18146da72de099f72be761b74fcfd3b4b9d45c17eda93a8b89266'    #（注册后生成）
ts.set_token(token)
pro=ts.pro_api()



class BasicInform():
    def __init__(self, symbol):
        '''
        加了判断语句,如果输入是数字,判断是代码.如果不是数字.判断是名字
        '''
        # if re.match(r'^\d{6}$',symbol):
        #     self.code = symbol
        #     self.name = self.getstockname()
        # elif re.match(r'^\D*$',symbol):
        #     self.name = symbol
        #     self.code = self.getstockcode()
        # self.close = self.getlatestprice()
        self.symbol = symbol
        stockinform = self.get_stock_inform()
        self.code = stockinform['code']
        self.name = stockinform['name']
        self.latestprice = stockinform['latestprice']
        self.ratio = stockinform['ratio']
        self.preclose = stockinform ['preclose']


    # def getstockname(self):
    #     stockinfo = ak.stock_individual_info_em(symbol=self.code)
    #     value = stockinfo['value']
    #     name = value[5]
    #     return name
    #
    # def getlatestprice(self):
    #     stockdata = ak.stock_zh_a_spot_em()
    #     index = stockdata[(stockdata.代码 == self.code)].index.tolist()
    #     price = stockdata.iloc[index]['最新价']
    #     return float(price)
    #
    # def getstockcode(self):
    #     data = pro.stock_basic(exchange='', list_status='L', name=self.name, field='ts_code')
    #     code = data['ts_code'][0]
    #     code = code[:6]
    #     return code

    def get_stock_inform(self):
        stock = qs.realtime_data(code=self.symbol)
        code = stock['代码'].values[0]
        name = stock['名称'].values[0]
        latestprice = stock['最新'].values[0]
        ratio = stock['涨幅'].values[0]
        preclose = stock['昨收'].values[0]
        dict = {'code':code, 'name':name, 'latestprice':latestprice, 'ratio':ratio, 'preclose':preclose}
        return dict



class ForShowStock(BasicInform):
    def __init__(self,symbol):
        super(ForShowStock, self).__init__(symbol)
        moreinform = self.get_more_inform()
        self.preclose = moreinform['preclose']
        self.ratio = moreinform['ratio']

    def get_more_inform(self):
        stock = qs.realtime_data(code=self.symbol)
        ratio = stock['涨幅'].values[0]
        preclose = stock['昨收'].values[0]
        dict = {'ratio':ratio, 'preclose':preclose}
        return dict



class PredictValue(BasicInform):
    '''
    上面的 函数 value_of_future ,用类的方法改写
    '''
    def __init__(self, code):
        super(PredictValue,self).__init__(code)
        fore_eps_list = self.calvoa()
        self.epsn = fore_eps_list[0]
        self.epsn1 = fore_eps_list[1]
        self.epsn2 = fore_eps_list[2]
        self.voa = fore_eps_list[3]
        self.voa_pre = 0

    def calvoa(self):
        fore_eps_df = ak.stock_profit_forecast_ths(symbol=self.code, indicator="预测年报每股收益")
        fore_eps_list = []
        for i in range(3):
            fore_eps_list.append(fore_eps_df.iloc[i, 3])
        price_evaluate = fore_eps_list[2] * (fore_eps_list[2] / fore_eps_list[1] - 1) * 100  # 预估2年后的估值
        price_evaluate = round(price_evaluate, 2) # 只保留2位小小数
        fore_eps_list.append(price_evaluate)
        return fore_eps_list


class StockInform():
    def __init__(self, symbol):
        self.symbol = symbol
        stockinform = self.get_stock_inform()
        self.code = stockinform['code']
        self.name = stockinform['name']
        self.latestprice = stockinform['latestprice']
        self.location  = self.get_location()
        self.category = self.get_category()

    def get_location(self):
        if re.match(r'^[568]', self.code):
            location = 'Shanghai'
        if re.match(r'^[0-3]', self.code):
            location = 'Shenzhen'
        return location

    def get_category(self):
        if re.match(r'^[15]', self.code):
            category = 'ETF'
        if re.match(r'^[02368]', self.code):
            category = 'Stock'
        return category

    def get_stock_inform(self):
        stock = qs.realtime_data(code=self.symbol)
        code = stock['代码'].values[0]
        name = stock['名称'].values[0]
        latestprice = stock['最新'].values[0]
        dict = {'code':code, 'name':name, 'latestprice':latestprice}
        return dict




class StockTrade(StockInform):
    '''
    计算交易费用
    1.印花税：成交金额的1‰ [4]  。2008年9月19日由向双边征收改为向出让方单边征收。受让者不再缴纳印花税。投资者在买卖成交后支付给财税部门的税收。上海股票及深圳股票均按实际成交金额的千分之一支付，此税收由券商代扣后由交易所统一代缴。债券与基金交易均免交此项税收。
    2.证管费：成交金额的0.002%双向收取
    3.证券交易经手费：A股，按成交金额的0.0487‰双向收取；B股，按成交额0.0487‰双向收取；基金，上海证券交易所按成交额双边收取0.045‰，深圳证券交易所按成交额0.0487‰双向收取；权证，按成交额0.045‰双向收取。
        A股2、3项收费合计称为交易规费，合计收取成交金额的0.0687‰，包含在券商交易佣金中。
    4.过户费（从2015年8月1日起已经更改为上海和深圳都进行收取）：这是指股票成交后，更换户名所需支付的费用。根据中国证券登记结算有限责任公司的发文《中国结算关于降低股票交易过户费收费标准的通知 [5]  》，自2022年4月29日起，统一下调为按照成交金额0.01‰双向收取。
    5.券商交易佣金：最高不超过成交金额的3‰，最低5元起，单笔交易佣金不满5元按5元收取。
    '''
    def __init__(self, symbol, quantity, price, mark):
        super(StockTrade, self).__init__(symbol)
        self.quantity = quantity
        self.price = price
        self.mark = mark.lower()
        self.stock_cost = self.get_stock_cost()
        self.commission = self.get_commission()   #佣金
        self.tranfer_fee = self.get_transfer_fee()  # 过户费
        self.stamp_tax = self.get_stamp_tax()   # 印花税
        # self.management_fee = self.get_management_fee() # 证管费
        # self.handle_fee = self.get_handle_fee() #经手费
        self.ammount = self.get_ammount()

    def get_stock_cost(self):
        cost = self.price * self.quantity
        cost = round(cost, 2)
        return cost

    def get_commission(self):
        ratio = 2/10000
        kzz = self.code[0]=='1' and (self.code[1] == '1' or '2')
        commission = self.stock_cost * ratio
        if  commission < 5 and (not kzz):
            commission = 5
        commission = round(commission, 2)
        return commission

    def get_transfer_fee(self):
        ratio = 0.01/1000
        if self.code[0] == '6':
            transfer_fee = self.stock_cost * ratio
        # if self.code[0] == '1' or self.code[0] == '5':
        else:
            transfer_fee = 0
        transfer_fee = round(transfer_fee, 2)
        return transfer_fee

    def get_stamp_tax(self):
        ratio = 1/1000
        # stamp_tax = 0
        # if self.mark == 'sell'  :     #卖的时候收,ETF不收
        stamp_tax = self.stock_cost * ratio
        # if self.code == '1' or self.code == '5':
        #     stamp_tax =0
        stamp_tax = round(stamp_tax, 2)
        return stamp_tax
    #
    # def get_management_fee(self):
    #     ratio = 0.002/100
    #     management_fee = self.stock_cost * ratio
    #     if self.code == '1' or self.code == '5':
    #         management_fee = 0
    #     management_fee = round(management_fee, 2)
    #     return management_fee
    #
    # def get_handle_fee(self):
    #     if self.code[0] == '5':
    #         ratio = 0.045 / 1000
    #     else:
    #         ratio = 0.0487/1000
    #     handle_fee = self.stock_cost * ratio
    #     handle_fee = round(handle_fee, 2)
    #     return handle_fee

    def get_ammount(self):
        if self.mark == 'buy':
            ammount = self.stock_cost + (self.commission + self.tranfer_fee)
        if self.mark == 'sell':
            if self.code[0] == '1' or '5':    #卖的时候收,可转债，ETF不收印花税
                ammount = self.stock_cost - (self.commission + self.tranfer_fee )
            else:
                ammount = self.stock_cost -(self.commission + self.tranfer_fee  + self.stamp_tax)
        ammount = round(ammount,2)
        return ammount



# class Indexstrategy():
#     def __init__(self):
#         codelist = ['510050', '159915']
#         self.df = qs.get_data(codelist,self.startday)
#         self.szratio  = self.get_ratio(code = '510050')
#         self.cybratio = self.get_ratio(code = '159915')
#         self.startday = self.get_startday()
#
#     def get_startday(self):
#         import datetime
#         deltatime = datetime.timedelta(days=40)
#         foreday = (datetime.datetime.today() - deltatime).strftime('%Y%m%d')
#         return foreday
#
#     def get_ratio(self,code):
#         df = self.df[self.df['code']==code]
#         closelist = df['close'].values
#         ratio = (closelist[-1]-closelist[-20])/closelist[-20]
#         return ratio
#



