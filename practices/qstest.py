import qstock as qs
import  pandas as pd
import akshare as ak

def main():
    # codelist = ['300684',"000001",'512400','180202','508009','014531','016709','164906','008359','163406']
    # df  = qs.realtime_data(code=codelist)
    # print(df)
    # price_list =[]
    # for i in range(len(codelist)):
    #     li = []
    #     # index = stockdata[(stockdata.代码 == i)].index.tolist()
    #     price = df.iloc[i]['最新']
    #     ratio = df.iloc[i]['涨幅']
    #     preclose = df.iloc[i]['昨收']
    #     li.append(float(price))
    #     li.append(ratio)
    #     li.append(float(preclose))
    #
    #     price_list.append(li)
    #
    # print(price_list)
    # name  = df['名称'][0]
    # # = name1[0]
    # print (name)
    # print(type(name))
    # # print(name1[])
    # print(df['名称'])

    # df.to_csv('300684',sep= ',' ,index= False ,header= True)
    # df1=qs.get_data('601318')
    # print(df1.head())

    code  = '600036'
    df = qs.realtime_data(code = code)
    name = df['名称']
    name1 = name.values[0]
    name2 = df.iloc[0]
    name3 = name2[1]
    print(df)
    print(name)
    print(name1)
    print(name2)
    print(name3)

def getaCSVFile():
    df=qs.get_data('601318',start='20220101')
    df.to_csv('601318.csv')
    # print (df)


if __name__ == '__main__':
    main()