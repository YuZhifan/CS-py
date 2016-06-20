#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

import socket               # 导入 socket 模块
import threading
import time
import os

s = socket.socket()         # 创建 socket 对象
host = socket.gethostname()    # 服务器IP
port = 12345                # 设置端口号
s.connect((host, port))


def listen():
    rec=s.recv(1024).decode("utf8")
    while(rec!=""):
        print(rec)
        rec=s.recv(1024).decode("utf8")


def getin():
    time.sleep(0.3)
    string=input()
    while(string!="quit"):
        time.sleep(0.3)
        s.send(string.encode("utf8"))
        string=input()
    s.close()
    
        
name=input('请输入用户名：')
pwsd=input('请输入密码：')
namepwsd=name+'#'+pwsd
#print(namepwsd)
s.send(namepwsd.encode("utf8"))
print(s.recv(1024).decode("utf8"))

#threading.Thread(target=listen).start()
threading.Thread(target=getin).start()
try:
    rec=s.recv(1024).decode("utf8")
    while(rec!=""):
        print(rec)
        rec=s.recv(1024).decode("utf8")
except ConnectionAbortedError:
    print("已断开连接")
    print("重启中...")
    time.sleep(1)
    os.system("python client.py")
    
s.close()

