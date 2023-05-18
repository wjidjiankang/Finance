from django.test import TestCase

# Create your tests here.


from django.db import models

# Create your models here.


class Userinfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Stock(models.Model):
    code = models.CharField(max_length = 6)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length = 10)
    qty = models.DecimalField(decimal_places=2, max_digits=10)
    amt = models.DecimalField(decimal_places=2, max_digits=12)


class Fund(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=10)
    mark = models.CharField(max_length=4)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    amt = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now_add=True)


