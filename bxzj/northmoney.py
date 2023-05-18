import akshare as ak
import pandas as pd
import sqlite3
from xlutils.copy import copy
import xlrd
import os


def main():

    stock_em_hsgt_hold_stock_df = ak.stock_hsgt_hold_stock_em(market="北向", indicator="今日排行")
    # print(stock_em_hsgt_hold_stock_df)
    # print(stock_em_hsgt_hold_stock_df.describe())
    # codedf = pd.read_csv('code100.csv')
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(base_dir,'scode.xls')
    dbfile = os.path.join(base_dir,'northmoney.db')

    # file = 'scode.xls'
    codedf = pd.read_excel(file, dtype={'code': str})
    print(codedf)
    codelist = codedf['code'].values
    # 进行准备写入excel的操作
    rb = xlrd.open_workbook(file, formatting_info=True)
    ws = rb.sheets()[1]
    nrows = ws.nrows  # 总行数
    book = copy(rb)
    sheet = book.get_sheet(1)
    # print(nrows)
    #连接数据库
    conn = sqlite3.connect(dbfile)

    for code in codelist:
        # code = '300750'
        # print(code)
        #获取数据
        index = stock_em_hsgt_hold_stock_df[(stock_em_hsgt_hold_stock_df.代码 == code)].index.tolist()
        # print (index)
        name = stock_em_hsgt_hold_stock_df.iloc[index]['名称'].tolist()[0]
        add_qty = stock_em_hsgt_hold_stock_df.iloc[index]['今日增持估计-股数'].tolist()[0]
        add_amt = stock_em_hsgt_hold_stock_df.iloc[index]['今日增持估计-市值'].tolist()[0]
        add_ratio = stock_em_hsgt_hold_stock_df.iloc[index]['今日增持估计-占总股本比'].tolist()[0]
        catalog = stock_em_hsgt_hold_stock_df.iloc[index]['所属板块'].tolist()[0]
        date = stock_em_hsgt_hold_stock_df.iloc[index]['日期'].tolist()[0]
        # print(add_amt)
        print('今日({}){}(代码:{})增持{}万股,金额{}万元,占总股本的千分之{}'.format(date, name, code, add_qty, add_amt, add_ratio))

        #写入数据库
        insert_sql = '''
            INSERT INTO north(CODE,Name,add_qty,add_amt,add_ratio,catalog,date)
            Values('%s','%s','%f','%f','%f','%s','%s')''' % (code, name, add_qty, add_amt, add_ratio, catalog, date)
        conn.execute(insert_sql)

        #写入excel
        sheet.write(nrows, 0, code)
        sheet.write(nrows, 1, name)
        sheet.write(nrows, 2, add_qty)
        sheet.write(nrows, 3, add_ratio)
        sheet.write(nrows, 4, add_amt)
        sheet.write(nrows, 5, catalog)
        sheet.write(nrows, 6, date)
        # sheet.write(nrows, 2, add_qty)
        nrows = nrows + 1
    conn.commit()
    conn.close()
    book.save(file)


def ceate_database():
    conn = sqlite3.connect("northmoney.db")
    conn.execute('''CREATE TABLE north
        (CODE      TEXT  NOT NULL,
        Name      TEXT  NOT NULL,
        add_qty     real   NOT NULL,
        add_amt     real   NOT NULL,
        add_ratio   real   NOT NULL,
        catalog     TEXT  NOT NULL,
        date        TEXT  NOT NULL);''')
    conn.close()
'''
增持估计-股数	float64	注意单位: 万; 主要字段名根据 indicator 变化
增持估计-市值	float64	注意单位: 万; 主要字段名根据 indicator 变化
增持估计-市值增幅	object	注意单位: %; 主要字段名根据 indicator 变化
增持估计-占流通股比	float64	注意单位: ‰; 主要字段名根据 indicator 变化
增持估计-占总股本比	float64	注意单位: ‰; 主要字段名根据 indicator 变化
所属板块	object	-
日期	object	-
'''

if __name__ == '__main__':
    main()
