#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

import socket               # 导入 socket 模块
import threading			#导入 threading 模块
import time				#导入 time 模块
import os				#导入 os 模块
from tkinter import *   #引用Tk模块

def listen():			#监听接收线程
    try:
        while True:
            rec=s.recv(1024).decode("utf8")
            if(rec!=""):
                print(rec)
                display(rec+"\n")
    except ConnectionAbortedError:
        print("已断开连接")
    except OSError:
        pass

def getin():		#监听输入线程(命令用，图形化界面不用)
    time.sleep(0.3)
    while True:
        string=input()
        if(string=="showuser"):
            pass
        else:   
            time.sleep(0.3)
            s.send(string.encode("utf8"))
    
s = socket.socket()         # 创建 socket 对象
host = socket.gethostname()    # 服务器IP
port = 12345                # 设置端口号
s.connect((host, port))			#连接服务器


name=input('请输入用户名：')
pwsd=input('请输入密码：')
namepwsd=name+'#'+pwsd
#print(namepwsd)
s.send(namepwsd.encode("utf8"))
print(s.recv(1024).decode("utf8"))

root = Tk()             #初始化Tk()
root.title("Client")
root.geometry('400x300')
root.resizable(width=False, height=False) #宽不可变, 高可变,默认为True

scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill=Y )
text = Text(root,width=400,height=17,yscrollcommand = scrollbar.set)
text.pack(side=TOP)
var = StringVar()
def sendmessage():
    #text.insert(END,var.get()+"\n")
    try:
        s.send(var.get().encode("utf8"))
        var.set("")
    except ConnectionAbortedError:
        print("请关闭重启")
        display("请关闭重启\n")
        
Button(root, text="send", command = sendmessage).pack(side=BOTTOM)

e = Entry(root, textvariable = var)
e.pack(side=BOTTOM)

var.set("hello")
def display(rec):
    text.insert(END,rec)

thread3=threading.Thread(target=listen)    
#thread1=threading.Thread(target=getin)
#thread1.start()
thread3.start()

root.mainloop()         #进入消息循环

s.close()
#thread2.stop()
#thread1.stop()
thread3.stop()

