#coding:utf-8
import re
from django import forms
from django.forms import ValidationError
from models import User
class Register(forms.Form):
    username = forms.CharField(max_length = 6,min_length = 2,label = "用户名",widget = forms.TextInput(attrs = {"class":"form-control","placeholder":"用户名"}))
    password = forms.CharField(max_length = 32,min_length = 6,label = "密码",widget = forms.PasswordInput(attrs = {"class":"form-control","placeholder":"密码"}))
    phone = forms.CharField(max_length = 11,min_length = 11,label = "手机号",widget = forms.TextInput(attrs = {"class":"form-control","placeholder":"手机号"}))
    email = forms.EmailField(max_length = 32,label = "用户邮箱",widget = forms.TextInput(attrs = {"class":"form-control","placeholder":"用户邮箱"}))
    photo = forms.ImageField(label = "用户头像")

    #用户名唯一
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            username = User.objects.get(username = username)
        except:
            return username
        else:
            raise ValidationError("用户名不可以重复")
    #电话号唯一
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        try:
            user = User.objects.get(phone = phone)
        except:
            return phone
        else:
            raise ValidationError("用户手机号不可以重复")
    #密码的构成
    def clean_password(self):
        """
        表单验证常用的方法 raise
        常用的错误类型 ValidationError
        :return:
        """
        password = self.cleaned_data.get("password") #获取要判断的值
        if password.isdigit():
            raise ValidationError("密码不可以由纯数字组成")
        elif password.isalpha():
            raise ValidationError("密码不可以由纯字母数字组成")
        else:
            return password #返回要判断的值
    #email的格式
    def clean_email(self):
        email = self.cleaned_data.get("email")
        res = re.match(r"\w+@\w+\.[a-zA-Z]+",email)
        if res:
            return email
        else:
            raise ValidationError("邮箱格式错误")
