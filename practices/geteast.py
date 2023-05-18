import requests




def main():
    # url = 'https://data.eastmoney.com/hsgtcg/StockHdStatistics/300750.html'


    # 请求
    # URL: https: // datacenter - web.eastmoney.com / api / data / v1 / get?callback = jQuery112309138090049356766_1673689552585 & sortColumns = TRADE_DATE & sortTypes = -1 & pageSize = 50 & pageNumber = 1 & reportName = RPT_MUTUAL_HOLDSTOCKNORTH_STA & columns = ALL & source = WEB & client = WEB & filter = (
    #             SECURITY_CODE % 3D % 22300750 % 22)(TRADE_DATE % 3
    # E % 3
    # D % 272022 - 10 - 14 % 27)
    stockcode = '600519'

    url='https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112309138090049356766_1673689552585&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=50&pageNumber=1&reportName=RPT_MUTUAL_HOLDSTOCKNORTH_STA&columns=ALL&source=WEB&client=WEB&filter=(SECURITY_CODE%3D%22600519%22)(TRADE_DATE%3E%3D%272022-10-14%27)'
    url1='https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112309138090049356766_1673689552585&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=50&pageNumber=1&reportName=RPT_MUTUAL_HOLDSTOCKNORTH_STA&columns=ALL&source=WEB&client=WEB&filter=(SECURITY_CODE%3D%22'+stockcode+'%22)(TRADE_DATE%3E%3D%272022-10-14%27)'
    headers = {'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'}
    response = requests.get(url = url1,headers = headers)
    re = response.text
    a = re.split('[')[1]
    b = a.split('{')[1]
    c = b.split('}')[0]
    # print(re)
    # print(a)
    # print(b)
    code = c.split(',')[3].split(':')[1]
    name = c.split(',')[4].split(':')[1]
    close =  c.split(',')[7].split(':')[1]
    ratio = c.split(',')[10].split(':')[1]
    date = c.split(',')[2].split(':')[1]

    print(c)
    print(code)
    print(name)
    print(close)
    print(ratio)
    print(date)


if __name__ == '__main__':


    main()
