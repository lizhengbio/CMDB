#coding:utf-8

from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$',user_list),
    url(r'^registervalid/$', registervalid),
]