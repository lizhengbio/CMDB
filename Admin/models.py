#coding:utf-8
from django.db import models

class User(models.Model): #用户注册信息
    username = models.CharField(max_length = 32,verbose_name = "用户名")
    password = models.CharField(max_length = 32,verbose_name = "密码")
    phone = models.CharField(max_length = 32,verbose_name = "手机号")
    photo = models.ImageField(upload_to = "image",verbose_name = "用户头像")
    email = models.EmailField(max_length = 32,verbose_name = "用户邮箱")

class Permission(models.Model): #用户权限
    name = models.CharField(max_length = 32,verbose_name = "权限名称")
    description = models.TextField(verbose_name = "权限描述")
    url = models.CharField(max_length = 32,verbose_name = "URL")
    # obj_id = models.IntegerField(verbose_name = "权限对象")

class Permission_user(models.Model): #用户与权限关系表
    Permission_id = models.IntegerField(verbose_name = "权限id")
    User_id = models.IntegerField(verbose_name = "用户id")


# Create your models here.
