#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py

import socket               # 导入 socket 模块
import threading

clist=list()

def broadcast(string,c):
    #print("broadcast")
    for cl in clist:
        #if(c!=cl):
            #print(cl)
            cl.send(string.encode("utf8"))


def client(c,addr):
    flag=False
    name="null"
    #print ('连接地址：', addr)
    namepwsd=c.recv(1024).decode("utf8")
    namepwsd=namepwsd.split("#")
    name=namepwsd[0]
    pwsd=namepwsd[1]
    fo = open(r"D:\GitHub\CS-py\pswd.txt", "r+")    #读取用户表
    for  line in  fo.readlines():
        lines=line.split("#")
        if((lines[0]==name)&(lines[1]==pwsd)&(flag==False)):
            flag=True
        #print(name+pwsd)
        #print(lines[0]+lines[1])
        #print(flag)
    fo.close()
    if(flag==True):
        string="【系统】欢迎登陆,"+name
        print("【"+name+"】"+"登入")
        broadcast("【"+name+"】"+"登入",c)
    else:
        string="验证失败"
    c.send(string.encode("utf8"))
    try:
        string=c.recv(1024).decode("utf8")
        while(string):
            print("【"+name+"】"+string);
            broadcast("【"+name+"】"+string,c)
            string=c.recv(1024).decode("utf8")
    except socket.error:
        #print("wocuole")
        clist.remove(c)
        broadcast("【"+name+"】退出",c)
        print("【"+name+"】退出",c)
    c.close()
    



s = socket.socket()         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 12345                # 设置端口
s.bind((host, port))        # 绑定端口
s.listen(5)                 # 等待客户端连接
print("服务器启动...")
while True:
    c, addr = s.accept()     # 建立客户端连接。
    clist.append(c)
    threading.Thread(target=client,args=(c,addr)).start()    
