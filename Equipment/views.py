#coding:utf-8
import paramiko
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from models import *
from CMDB.views import getpage
from django.shortcuts import HttpResponseRedirect
from Admin.views import loginValid
import time
import datetime
from Admin.views import getmd5

def token_valid(fun): #接口请求token认证
    def inner(token,*args,**kwargs):
        result = ""
        try:
            t = Token.objects.get(value = token)
        except:
            result = "we have no token named %s" %token
        else:
            #把数据库里的时间转换成时间戳
            register_time = t.register
            register_times = time.mktime(register_time.timetuple())
            #把当前时间转换为时间戳
            now_times= time.time()
            num = now_times-register_times
            timeout = t.timeout
            if num > timeout:
                result = "your token is time out"
                t.delete()
            else:
                result = fun(*args,**kwargs)
        finally:
            return result
    return inner

def login(username,password):
    example_str = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ"
    result = {
        "statue":"error",
        "data":{
            "type":"error",
            "content":""
        },
    }
    try:
        u = Equipment.objects.get(user=username)
    except:
        result["data"]["type"] = "UserNameError"
        result["data"]["content"] = "we have no user named %s" % username
    else:
        db_password = u.Password
        if db_password == password:
            tk = "".join(random.sample(example_str,21))
            now = datetime.datetime.now()
            t = Token()
            t.usename = username
            t.value = tk
            t.register = now
            t.timeout = 3600
            try:
                t.save()
                result["statue"] = "success"
                result["data"]["type"] = "success"
                result["data"]["content"] = tk
            except Exception as e:
                result["data"]["type"] = "save mistake"
                result["data"]["content"] = "your token is not saved"
        else:
            result["data"]["type"] = "PasswordError"
            result["data"]["content"] = "your password is wrong"
    return result

@token_valid
def setData(ip,hostname,system,mac):
    equpment = Equipment.objects.get(IP = ip)
    equpment.hostname = hostname
    equpment.System = system
    equpment.Mac = mac
    equpment.save()
    return "set success"


def eq_list(request):
    if request.method == "GET":
        requestData = request.GET
        page = requestData.get("page")
        num = requestData.get("num")
        sql = "select * from equipment_equipment"
        if page and num:
            result = getpage(sql = sql,page = page,num = num)
        elif page :
            result = getpage(sql=sql, page=page)
        else:
            result = {
                "page_data": "",
                "page_range": ""
            }
    else:
        result = {
            "page_data": "",
            "page_range": ""
        }
    return JsonResponse(result)

@loginValid
def eq_list_page(request):
    eq_List = Equipment.objects.all()
    return render(request,"equipmentList.html",locals())

def eq_connect(request):
    """
    connect 方法实现 远程登录
    connect 方法实现 脚本上传
    connect 方法实现 脚本远程执行
    :param request:
    :return:
    """
    result = {"state":"error","data":""}
    if request.method == "POST":
        data = request.POST
        ip = data.get("ip")
        port = data.get("port")
        username = data.get("username")
        password = getmd5(data.get("password"))
        if ip and port and username and password:
            equpment = Equipment()
            equpment.IP = ip
            equpment.user = username
            equpment.Password = password
            equpment.save()
            try:
                trans = paramiko.Transport(ip,port)
                trans.connect(username = username,password = password)

                sftp = paramiko.SFTPClient.from_transport(trans) #用于文件的上传和下载的sftp服务
                ssh = paramiko.SSHClient() #远程执行命令的服务
                ssh._transport = trans
                with open("sftpDir/settings.py","w") as f:
                    f.write("#!/usr/bin/python"+"\n"+"USER = "+ username + "\n" + "PASSWORD = "+password)
                #创建目录
                stdin,stdout,stderr = ssh.exec_command("mkdir CMDBClient")
                #上传文件
                sftp.put("sftpDir/getData.py","/root/CMDBClient/getData.py")
                sftp.put("sftpDir/sendData.py", "/root/CMDBClient/sendData.py")
                sftp.put("sftpDir/main.py", "/root/CMDBClient/main.py")
                sftp.put("sftpDir/main.py","/root/CMDBClient/settings.py")
                #调用脚本
                stdin, stdout, stderr = ssh.exec_command("python /root/CMDBClient/main.py")
                trans.close()
                equpment.Statue = "True"
            except:
                equpment.Statue = "False"
            finally:
                equpment.save()
        else:
            pass
    else:
        pass

    return JsonResponse(result)

def eq_api(request):
    result = {
        "statue":"error",
        "data":{
            "type":"error",
            "content":""
        },
    }
    if request.method == "POST":
        types = request.POST.get("type")
        if types:
            if types == "login":
                try:
                    data = request.POST["result"]
                    data = json.loads(data)
                    username = data["username"]
                    password = data["password"]
                except keyError as e:
                    result["data"]["type"] = "KeyError"
                    result["data"]["content"] = str(e)
                else:
                    if username and password:
                        result = login(username,password)
                    else:
                        result["data"]["type"] = "EmptyError"
                        result["data"]["content"] = "username and password not be null"
            elif types == "sendData":
                token = request.POST.get("token")
                if token:
                    data = request.POST["result"]
                    data = json.loads(data)
                    ip = request.META["REMOTE_ADDR"]
                    hostname = data.get("get_hostname")
                    system = data.get("get_system")
                    mac = data.get("get_mac")
                    result["statue"] = "success"
                    result["data"]["type"] = "success"
                    result["data"]["content"] = setData(token,ip,hostname,system,mac)
                else:
                    result["data"]["type"] = "TokenError"
                    result["data"]["content"] = "Token not be null"
            else:
                result["data"]["type"] = "UnKnow"
                result["data"]["content"] = "UnKnow your command"
        else:
            result["data"]["type"] = "UnKnow"
            result["data"]["content"] = "UnKnow your method"
    else:
        result["data"]["content"] = "the request must be post"
    return JsonResponse(result)


terminal_dict = {}
def shell(request):
    if request.method == "GET":
        id = request.GET["id"]
        if id:
            equipment = Equipment.objects.get(id = int(id))
            ip = equipment.IP
            username = equipment.user
            password = equipment.Password
            if ip and username and password:
                try:
                    result = {"status":"success","ip":ip,}
                    trans = paramiko.Transport(sock = (ip,22))
                    trans.connect(
                        username = username,
                        password = password
                    )
                    ssh = paramiko.SSHClient()
                    ssh._transport = trans
                    terminal = ssh.invoke_shell()
                    terminal.settimeout(2)
                    terminal.send("\n")
                    login_data = ""
                    while True:
                        try:
                            recv = terminal.recv(9999)
                            if recv:
                                login_data += recv
                            else:
                                continue
                        except:
                            break
                    result["data"] = login_data.replace("\r\n","<br>")
                    terminal_dict[ip] = terminal
                    response = render(request, "shell.html", locals())
                    response.set_cookie("ip",ip)
                    return response
                except Exception as e:
                    print(e)
                    return HttpResponseRedirect("/eq/")


def command(request):
    ip = request.COOKIES.get("ip")
    if ip:
        if request.method == "GET":
            cmd = request.GET.get("command")
            if cmd:
                terminal = terminal_dict[ip]
                terminal.send(cmd+"\n")
                login_data = ""
                while True:
                    try:
                        recv = terminal.recv(9999)
                        if recv:
                            line_list = recv.split("\r\n")
                            result_list= []
                            for line in line_list:
                                l = line.replace(u"\u001B","").replace("[01;34m","").replace("[0m","").replace("[01;32m","").replace("[01;31m","")
                                result_list.append(l)
                            login_data = "<br>".join(result_list)
                        else:
                            continue
                    except:
                        break
                    result = {"result":login_data}
                    return JsonResponse(result)
            else:
                return HttpResponseRedirect("/eq/")
        else:
            return HttpResponseRedirect("/eq/")
    else:
        return HttpResponseRedirect("/eq/")
import random

# def add_eq(request):
#     for i in range(100):
#         e = Equipment()
#         e.hostname = "localhost_%s"%i
#         e.IP = "192.168.1.%s"%(i+2)
#         e.System = random.choice(["win7_32","win7_64","centos.6_32","centos.7",])
#         e.Statue = random.choice(["True","False"])
#         e.Mac = random.choice(["00:0c:29:92:85:4e","00:0c:29:5b:2a:a1"])
#         e.user = "root"
#         e.Password = "123"
#         e.save()
#     return JsonResponse({"statue":"ahh"})


# Create your views here.
