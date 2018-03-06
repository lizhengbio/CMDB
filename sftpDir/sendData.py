#!/usr/bin/python
#coding:utf-8

import json
import requests
from settings import *

url = "http://192.168.1.104:8000/eq/eq_api"

def login():
    login_string = json.dumps({
        "username":USER,
        "password":PASSWORD
    })
    login_data = {
        "type":"login",
        "result":login_string,
        "token":""
    }
    response = requests.request("POST",url = url, data = login_data)
    content = json.loads(response.content)
    token = content["data"]["content"]
    return token

def sendData(data,token):
    set_json_data = json.dumps(set_data)
    send_data = {
        "type":"sendData",
        "result":set_json_data,
        "token":token
    }
    response = requests.request("POST",url=url,data=send_data)
    content = json.loads(response.content)
    return content


