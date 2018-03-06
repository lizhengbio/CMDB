#coding:utf-8
from django.shortcuts import render
from forms import Register
from models import User
from django.http import JsonResponse
import hashlib
from PIL import Image
from django.http import HttpResponseRedirect
import re
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def registervalid(request):
    result = {"statue":"error","data":""}
    if request.method == "POST":
        if "phone" in request.POST.keys():
            try:
                phone = request.POST["phone"]
                if len(phone) == 11:
                    u = Users.objects.get(phone=phone)
                    result["data"] = "该手机号已注册"
                elif len(phone) != 11:
                    result["data"] = "手机号位数错误"
            except:
                result["statue"] = "success"
                result["data"] = "ok"
        elif "password" in request.POST.keys():
            password = request.POST["password"]
            if password.isdigit():
                result["data"] = "密码不能由纯数字组成"
            elif password.isalpha():
                result["data"] = "密码不能由纯字母组成"
            elif len(password) < 6:
                result["data"] = "密码位数不能低于6位"
            else:
                result["statue"] = "success"
                result["data"] = "ok"
        elif "email" in request.POST.keys():
            email = request.POST["email"]
            res = re.match(r"\w+@\w+\.[a-zA-Z]+",email)
            if res:
                result["statue"] = "success"
                result["data"] = "ok"
            else:
                result["data"] = "邮箱格式错误"
    return JsonResponse(result)

def getmd5(password):
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        c_phone = cookie.get("phone")
        s_phone = request.session.get("phone")
        if c_phone and c_phone == s_phone :
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login")
    return inner



def logout(request):
    pass

@loginValid
def user_list(request):
    if request.method == "POST":
        data = request.POST
        img = request.FILES
        register = Register(data,img)
        if register.is_valid(): #检测提交数据是否正常
            validData = register.cleaned_data
            username = validData.get("username")
            password = validData.get("password")
            phone = validData.get("phone")
            email = validData.get("email")
            photo = img.get("photo")
            name = "static/img"+photo.name
            img = Image.open(photo)
            img.save(name)

            user = User()
            user.username = username
            user.password = getmd5(password)
            user.phone = phone
            user.email = email
            user.photo = "img/"+photo.name
            user.save()
    else:
        register = Register()

    return render(request,"userList.html",locals())

def user_alter(request):
    pass

def user_drop(request):
    pass

# Create your views here.
