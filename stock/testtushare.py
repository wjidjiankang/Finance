import tushare as ts
import datetime

token='dbc18146da72de099f72be761b74fcfd3b4b9d45c17eda93a8b89266'    #（注册后生成）
ts.set_token(token)
pro=ts.pro_api()



def main():
    """Run administrative tasks."""
    print('this is main function')
    df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20221202', end_date='20221203')
    print(df)


def getsymbol(code):
    if len(code) == 6:
        if code[0] == '6':
            codeforname = code+'.SH'
        elif code[0] == '0' or code[0] == '3':
            codeforname =code + '.SZ'
    return codeforname



def getname(code):
    codeforname = getsymbol(code)
    data = pro.stock_basic(exchange='', list_status='L', ts_code=codeforname, fields='name')
    name = data['name'][0]
    return name



def getprice (code):
    symbol = getsymbol(code)
    today = datetime.datetime.now().strftime('%Y%m%d')
    df = pro.daily(ts_code=symbol, start_date=today, end_date=today)
    price =df['close'][0]
    # price = float(close)
    return price






if __name__ == '__main__':
    main()
    name = '东方财富'
    data = pro.stock_basic(exchange='', list_status='L', name = name,field='ts_code')
    code  = data['ts_code'][0]
    code = code[:6]
    print (code)

