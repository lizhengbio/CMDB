#!/usr/bin/python
#coding:utf-8

import getData
from sendData import sendData

method_list = dir(getData)
method_dict = getData.__dict__#以字典的形式，对象的方法名称做键，属性本身做值
result_dict = {}
for method in method_list:
    if method.startswith("get"):
       result_dict[method] = method_dict[method]()

#sendData(result_dict)
if __name__ == "__main__":
    # print(result_dict)
    token = login()
    sendData(result_dict,token)
