#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py

import socket               # 导入 socket 模块
import threading

clist=list()    #存储在线客户端
ulist=list()    #存储在线用户

def broadcast(string,c):
    #print("broadcast")
    for cl in clist:
        #if(c!=cl):   #是否广播给自己
            #print(cl)
        cl.send(string.encode("utf8"))


def client(c,addr):
    flag=False   #验证标示符,默认为False
    name="null"     #用户名
    #print ('连接地址：', addr)
    namepwsd=c.recv(1024).decode("utf8")
    namepwsd=namepwsd.split("#")
    name=namepwsd[0]
    pwsd=namepwsd[1]
    fo = open(r"D:\GitHub\CS-py\pswd.txt", "r+")    #读取用户表
    for  line in  fo.readlines():   #账号密码验证
        lines=line.split("#")
        if((lines[0]==name)&(lines[1]==pwsd)&(flag==False)):
            flag=True
        #print(name+pwsd)
        #print(lines[0]+lines[1])
        #print(flag)
    fo.close()
    if(flag==True):
        string="【系统】欢迎登陆,"
        print("【"+name+"】"+"登入")
        ulist.append(name)
        broadcast("【"+name+"】"+"登入",c)
        c.send(string.encode("utf8"))
    else:
        string="验证失败"
        #验证失败处理
        c.send("已断开连接".encode("utf8"))
        c.send("请关闭在开启".encode("utf8"))
        c.close()
        print("【"+name+"】密码验证错误")
    try:
        while True:
            string=c.recv(1024).decode("utf8")
            if(string=="showuser"):
                ustr="【系统】在线用户："
                for ul in ulist:
                    ustr=ustr+"【"+ul+"】,"
                c.send(ustr.encode("utf8"))
                #print (clist)
            else:
                print("【"+name+"】"+string);
                broadcast("【"+name+"】"+string,c)
    except (ConnectionAbortedError,ConnectionResetError):
        #print("wocuole")
        clist.remove(c)
        ulist.remove(name)
        broadcast("【"+name+"】已退出",c)
        print("【"+name+"】已退出")
    except OSError:pass
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
