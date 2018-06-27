from django.conf.urls import url,include
from django.contrib import admin
from .views import userviews
urlpatterns = [
    url(r'^$',userviews.index,name='myadmin'),
    url(r'^add/$',userviews.add,name='myadd'),
    url(r'^list/$',userviews.list,name='mylist'),
    url(r'^edit/$',userviews.edit,name='myedit'),
    url(r'^delete/$',userviews.delete,name='mydelete')
]
