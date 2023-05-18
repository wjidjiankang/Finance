# from stock.myinform import BasicInform,PredictValue
from stock import myinform

code = '600036'
name = '东方财富'
symbol = '600000'

stock1 = myinform.PredictValue(code)
print(stock1.name,stock1.voa)

stock2 = myinform.PredictValue(name)
print(stock2.code,stock2.voa)

stock3 = myinform.PredictValue(symbol)
print(stock3.name, stock3.voa)

print(myinform.Indexstrategy.szratio,myinform.Indexstrategy.cybratio)