import baostock as bs
import pandas as pd
import  re

# 登陆系统
lg = bs.login()
# 显示登陆返回信息


# 获取证券基本资料
rs = bs.query_stock_basic(code="sh.600000")
# rs = bs.query_stock_basic(code_name="浦发银行")  # 支持模糊查询
# 打印结果集
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
print (data_list[0][1])
result = pd.DataFrame(data_list, columns=rs.fields)
# 结果集输出到csv文件

print(result)

li = '600001'
print(li[0])
an = re.match('^[0-9]*.$',li)
bn = re.match('^[0-9]?',li)
cn = re.match('^\d{6}$',li)

stockcode_regex = re.compile(r'\d{6}')
code  = stockcode_regex.search(li)


print(an.group())
print(bn)
print(cn)
print(code.group())

def getsymbol(code):
    if len(code) == 6:
        if code[0] == '6':
            codeforname = 'sh.' + code
        elif code[0] == '0' or code[0] == '3':
            codeforname ='sz.' + code
    return codeforname

import datetime
now = datetime.datetime.now().strftime('%Y-%m-%d')
print(now)
print(type(now))

rs = bs.query_history_k_data_plus("sh.600000",
    "date,time,code,open,high,low,close,volume,amount,adjustflag",
    start_date='2022-11-23',frequency= '30' ,end_date='2022-11-25', adjustflag="3")
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

print (result)




bs.logout()