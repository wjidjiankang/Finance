from django.shortcuts import render,redirect,HttpResponse
from users import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from users  import forms

# Create your views here.


def login(request):  # login函数
    if request.method == "GET":  # 前端如果是get请求
        return render(request, 'loginz.html')  # 返回HTML页面。
    elif request.method == "POST":  # 前端如果是post请求
        username = request.POST.get("username")  # 获取POST请求中的username值,字符串username要和前端form表单中的对应起来。
        password = request.POST.get("password")  # 获取POST请求中的password值，字符串password要和前端form表单中的对应起来。
        # request.POST.get返回的值是字符串，所以下面if中的判断是成立的。
        if username == "zy" and password == "12345":
            return redirect("/index/")
        else:  # 如果用户名或者密码错误，返回登录页面
            return render(request, "loginz.html")

