from django.contrib import admin
from django.urls import path,re_path,include
from users import views
from django.contrib.auth.views import login_required,auth_login
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

app_name = 'users'

urlpatterns = [

    path('login/',LoginView.as_view(template_name='login.html'),name='login'),
    # path('loginz/', views.loginz),
    # path('login', login.enterLoginPage),
    # path('loginAction', login.loginAction),



]