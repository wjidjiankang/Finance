from django.db import models

# Create your models here.


class Userinfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=40)
    mark = models.CharField(max_length=4,default='Buy')
    # quantity = models.DecimalField(max_digits=8, decimal_places=0,default=0)
    quantity = models.FloatField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    sell_profit = models.DecimalField(max_digits=10, decimal_places=3,default=0)


class StockInHand(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=40)
    # quantity = models.DecimalField(max_digits=8, decimal_places=0,default=0)
    quantity = models.FloatField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=3)
    price = models.DecimalField(max_digits=9, decimal_places=2,default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    profit_today = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    ratio  = models.FloatField()
    value = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    value_proportion = models.DecimalField(max_digits=4, decimal_places= 2, default= 0.00)

class StockProfitbyOp(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=40)
    # quantity = models.DecimalField(max_digits=8, decimal_places=0, default=0)
    quantity = models.FloatField()
    cost = models.DecimalField(max_digits=10, decimal_places=3)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(auto_now_add=True)
    ttlquantity=  models.DecimalField(max_digits=8, decimal_places=0, default=0)


class myText(models.Model):
    id = models.AutoField(primary_key=True)
    date_add = models.DateTimeField(auto_now_add=True)
    mytext = models.TextField()
    class Meta:
        verbose_name_plural = 'entries'
    def __str__(self):
        return self.mytext[:50] + '...'


# class PEGData(models.Model):
#     id = models.AutoField(primary_key=True)
#     # id = models.IntegerField(primary_key=True)
#     code = models.CharField(max_length=6)
#     name = models.CharField(max_length=40)
#     reportqty = models.IntegerField()
#     profit_n = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
#     profit_n1 = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
#     profit_n2 = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
#     profit_n3 = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
#     GRR = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
#     PEttm = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
#     PEG  = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)



class ValueOfAssenment(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20, blank=True)
    close = models.DecimalField(max_digits=10, decimal_places=3)
    eps_n = models.DecimalField(max_digits=10, decimal_places=3)
    eps_n1 = models.DecimalField(max_digits=10, decimal_places=3)
    eps_n2 = models.DecimalField(max_digits=10, decimal_places=3)
    voa = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateField(auto_now_add=True)



