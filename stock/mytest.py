import baostock as bs
import requests
from bs4 import BeautifulSoup
import html5lib

import tushare as ts
token='dbc18146da72de099f72be761b74fcfd3b4b9d45c17eda93a8b89266'    #（注册后生成）
ts.set_token(token)
pro=ts.pro_api()

df = pro.daily(ts_code='000001.SZ', start_date='20221126', end_date='20221126')
df2  = pro.stock_basic(exchange='', list_status='L',ts_code='000001.SZ', fields='name')
# name = df2.iloc[:,2][0]
# price = df['pre_close']
data = df2['name'][0]
# price = df['close']

print (data)
print ('*'*100)
print (df)
print ('*'*100)
print(df2)
print ('*'*100)
# print(name)
# print(price)
# print(type(price))




def getprice (code):
    symbol = code
    df = pro.daily(ts_code=symbol, start_date='20221126', end_date='20221126')
    close =df['pre_close'][0]
    price = float(close)
    return price
try :
    b = getprice('000001.SZ')
except:
    b = 0

print (b)
print (type(b))


import datetime
now = datetime.datetime.now().strftime('%Y%m%d')
print(now)
print(type(now))
# def getname(code):
#     if len(code) == 6:
#         if code[0] == '6':
#             codeforname = 'sh.' + code
#         elif code[0] == '0' or code[0] == '3':
#             codeforname = 'sz.' + code
#     bs.login()
#     # 显示登陆返回信息
#     # print('login respond error_code:' + lg.error_code)
#     # print('login respond  error_msg:' + lg.error_msg)
#     # 获取证券基本资料
#
#     rs = bs.query_stock_basic(code=codeforname)
#     data_list = []
#     while (rs.error_code == '0') & rs.next():
#         # 获取一条记录，将记录合并在一起
#         data_list.append(rs.get_row_data())
#     name = data_list[0][1]
#     bs.logout()
#     return name
#
# name = getname('300125')
# print (name)

# url1 = 'https://finance.sina.com.cn/realstock/company/'
# code = 'sz300125'
# url2 = '/nc.shtml'
# url = url1+ code +url2
# url3 = 'http://emweb.securities.eastmoney.com/PC_HSF10/OperationsRequired/Index?type=web&code=sh600050'
#
# print(url)
# url = 'https://xueqiu.com/S/SZ002049'
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'}
# response = requests.get(url,headers = headers)
# contex = response.text
# print (contex)
#
# print('*'*100)
# soup = BeautifulSoup(contex,"html5lib")
#
#
#
#
# list = soup.find(class_ ="stock-current" ).getText()
# price = list[1:]
# # <div id="price" class="down">26.19</div>
# # <div class="stock-current"><strong>¥136.80</strong></div>
# a = soup.find_all('a')
# print (list)
# print(price)
# print(a)

print('*'*100)
def getpricesnowball(url):
    stock = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'}
    response = requests.get(url, headers=headers)
    contex = response.text
    soup = BeautifulSoup(contex, "html5lib")
    price_list = soup.find(class_="stock-current").getText()
    name_list = soup.find(class_='stock-name').getText()
    price = price_list[1:]
    n = len(name_list)
    name = name_list[:n-11]
    stock = {'name':name,'price':price}
    return stock

def getnamefromsnowball(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'}
    response = requests.get(url, headers=headers)
    contex = response.text
    # print(contex)
    soup = BeautifulSoup(contex, 'html5lib')
    list = soup.find(class_="stock-name").getText()
    n = len(list)
    name = list[:n - 11]
    # <span class="price_down blinkgreen">7.39</span>
    # ?<span class="price_down blinkgreen">7.39</span>
    # print(name)
    return name


url  = 'https://xueqiu.com/S/SZ002049'

price  = getpricesnowball(url)
name = getnamefromsnowball(url)
print (price)
print (price['price'])
print('*'*100)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'}
response = requests.get('http://basic.10jqka.com.cn/600036/worth.html', headers=headers)
contex = response.content
print (contex)