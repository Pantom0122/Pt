from django.conf.urls import url,include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$',views.index,name='myadmin'),
    url(r'^add/$',views.add,name='myadd'),
    url(r'^list/$',views.list,name='mylist'),
    url(r'^edit/$',views.edit,name='myedit'),
    url(r'^delete/$',views.delete,name='mydelete')
]
