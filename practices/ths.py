import requests

url = 'https://biz.finance.sina.com.cn/suggest/lookup_n.php?country=&q=%E4%B8%9C%E6%96%B9%E8%B4%A2%E5%AF%8C&name=%E4%B8%9C%E6%96%B9%E8%B4%A2%E5%AF%8C&t=keyword&c=all&k=%E4%B8%9C%E6%96%B9%E8%B4%A2%E5%AF%8C&range=all&col=1_7&from=channel'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'}
response = requests.get(url=url,headers = headers)
contex = response.text
print (contex)