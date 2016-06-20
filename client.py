#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

import socket               # 导入 socket 模块
import threading			#导入 threading 模块
import time				#导入 time 模块
import os				#导入 os 模块

s = socket.socket()         # 创建 socket 对象
host = socket.gethostname()    # 服务器IP
port = 12345                # 设置端口号
s.connect((host, port))			#连接服务器


def listen():			#监听接收线程
    while True:
        rec=s.recv(1024).decode("utf8")
        print(rec)

def getin():		#监听输入线程
    time.sleep(0.3)
    while True:
        string=input()
        if(string=="quit"):
            s.close()
            break
        else:   
            time.sleep(0.3)
            s.send(string.encode("utf8"))
    
        
name=input('请输入用户名：')
pwsd=input('请输入密码：')
namepwsd=name+'#'+pwsd
#print(namepwsd)
s.send(namepwsd.encode("utf8"))
print(s.recv(1024).decode("utf8"))

#threading.Thread(target=listen).start()    #选其一作为主线程
thread1=threading.Thread(target=getin)
thread1.start()

try:
    rec=s.recv(1024).decode("utf8")
    while(rec!=""):
        print(rec)
        rec=s.recv(1024).decode("utf8")
except ConnectionAbortedError:
    print("已断开连接")
    #print("重启中...")
    #time.sleep(1)
    #os.system("python client.py")
except OSError:
    pass
s.close()
