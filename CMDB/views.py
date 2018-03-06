#coding:utf-8
from django.shortcuts import render
from Admin.views import loginValid,getmd5
import random
from django.http import HttpResponseRedirect
from django.db import connection
from Admin.models import *

content = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz'

@loginValid
def index(request):
    return render(request,"index.html",locals())


def login(request):
    if request.method == "POST":
        data = request.POST
        phone = data.get("phone")
        password = data.get("password")
        valid_remember = data.get("remember")
        cookie_remember = request.COOKIES.get("key")
        if valid_remember == cookie_remember:
            try:
                u = User.objects.get(phone = phone)
            except:
                return HttpResponseRedirect("/login")
            else:
                post_password = getmd5(password)
                if post_password == u.password:
                    response = HttpResponseRedirect("/index")
                    response.set_cookie("phone",u.phone)
                    request.session["phone"] = u.phone
                    request.session["user_id"] = u.id
                    return response
                else:
                    return HttpResponseRedirect("/login")
        else:
            return HttpResponseRedirect("/login")
    else:
        v_data = "".join(random.sample(content,18))
        response = render(request,"login.html",locals())
        response.set_cookie("key",v_data)
        return response

def logout(request):
    c_phone = request.COOKIES.get("phone")
    s_phone = request.session.get("phone")
    if c_phone and s_phone:
        del request.COOKIES["phone"]
        del request.session["phone"]
    return HttpResponseRedirect("/login/")

def getpage(sql,page,num = 10):
    """
    :param sql: 每次查询的语句
    :param page: 当前的页码
    :param num: 每页数据的条数
    :return: 查询出来的数据
    """
    #对数据进行修整
    page = int(page)
    num = int(num)
    #查询当前页面的数据
    start_page = (page-1) * num
    page_data_sql = sql + " limit %s,%s"%(start_page,num)
    cur = connection.cursor() #实例化游标
    cur.execute(page_data_sql)
    page_data = cur.fetchall()
    desc = cur.description #表的字段
    data_list = [
        dict(zip([d[0] for d in desc],row))
        for row in page_data
    ]
    #查询总条数
    page_total_sql = "select count(f.id) from (%s) as f"%sql
    cur.execute(page_total_sql)
    nums = cur.fetchone()[0]

    if nums%num == 0:
        page_total = nums/num
    else:
        page_total = nums/num +1
    result = {
        "page_data":data_list,
        "page_range":range(page_total-1,0,-1)
    }
    return result










