#coding:utf-8

from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$',eq_list_page),
    url(r'eq_api',eq_api),
    url(r'eq_connect', eq_connect),
    url(r'eq_list', eq_list),
    url(r'shell',shell),
    url(r'cmd',command),
    # url(r'add_eq',add_eq),
]