from django.contrib import admin
from django.urls import path,re_path,include
from stock import views,dbtest,models
from stock import login


app_name = 'stock'
urlpatterns = [
    path('loginz/', views.loginz),
    path('', views.index,name = 'index'),
    path('login' , login.enterLoginPage),
    path('loginAction', login.loginAction),
    path('data_entry/',views.data_entry,name = 'data_entry'),
    re_path(r'buystock',views.buystock),
    # re_path(r'db_handle', views.db_handle),
    re_path(r'dbaseTest',dbtest.dbaseTest),
    #re_path(r'add_book',views.add_book),
    path('showstock/',views.showstock,name = 'showstock'),
    # path('sellstock/',views.sellstock),
    re_path(r'sellstock',views.sellstock),
    #path('index/', views.index),
    # path('caldcf',views.caldcf,name = 'caldcf'),
    path('caldcf/',views.caldcf, name = 'caldcf'),
    path('cal_dcf/',views.cal_dcf),
    # path('cal_dcf',views.cal_dcf),
    # path('getword',views.getword, name = 'getword'),
    path('getword/',views.getword,name = 'getword'),
    # path('get_word',views.get_word),
    # path('get_word/',views.get_word,name = 'get_word'),
    # path('showpeg',views.showpeg,name = 'showpeg'),
    # path('showpeg/',views.showpeg,name = 'showpeg'),
    # path('test',views.test),
    path('predict/', views.predict, name='predict'),
    path('stock_clearance/',views.stock_clearance, name='stock_clearance'),


   ]