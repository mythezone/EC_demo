#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Mythezone
# DATE: 2019/12/23 Mon
# TIME: 00:25:18

# DESCRIPTION: A server

import socket,sys,time,json#,os,time,argparse,json
from multiprocessing import Process#,Manager,Lock,Queue
from utils import cprint
from message import reg_msg,par_msg

class server(Process):
    def __init__(self,myaddr,master=None,role='worker',links=10):
        Process.__init__(self)
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.myaddr=myaddr
        self.master=master
        self.links=links
        self.role='worker'
        self.func_route={}
        # print("self.role:",self.role)
        self.bind()

        if master!=None:
            self.register()

    def bind(self):
        try:
            self.s.bind(self.myaddr)
            print("INFO: Server %s:%s will run on - IP : %s, PORT : %s."%(cprint(self.name,'yellow',False),\
                    cprint(self.role,'sky',False),cprint(self.myaddr[0],'Green',False),cprint(self.myaddr[1],'Green',False)))
        except Exception as e:
            print("Bind Error.\n",e)
            sys.exit()

    def add(self,msg_type,func):
        pass

    def add_work(self,key_word,func):
        self.func_route[key_word]=func
        return

    def register(self):
        msg=reg_msg(self.myaddr)
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        count=0
        while True:
            
            try:
                s.connect(self.master)
                s.send(msg)
                r=s.recv(1024)
                tmp=cprint("RECV:",'blue',False)
                print("{}{}".format(tmp,cprint(r.decode(),'green',False)))
                break
            except:
                cprint("Connect failed, try to connect after 2 seconds.",'red')
                count+=1
                if count==5:
                    cprint("Error: Cannot connect to the master, please check if the server is running.",'bred')
                    sys.exit()
                time.sleep(2)
                continue
    
    def hello(self,addr):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(addr)
        s.send("hello".encode())
        s.close()

    def tester(self,addr):
        print("The target work is :{}".format(cprint(addr,'yellow',False)))
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(addr)
        # s.send("hello".encode())
        msg=[
                {
                    "type":"file",
                    "content":{
                        "url":'accident.txt',
                        "md5":"fdkajflfdkajlsa"
                    }
                },
                {
                    "type":"start",
                    "content":
                    {
                        "population":[[5,6,8],[4,8,6,9],[0,24,6],[2],[8,5]],
                        "iteration":100,
                        "k":5
                    }
                },
                {
                    "type":"stop",
                    "content":{}
                },
                {
                    "type":"comment",
                    "content":{
                        "status":"succeed",
                        "msg":"success to register"
                    }
                },
                {
                    "type":"query",
                    "content":{}
                }

            ]
        order=0
        while True:
            index=input("Input the index of the message you want to send (0-4):")
            # index= order
            # order+=1
            try:
                index=int(index)
            except:
                cprint("Illegal input , please check your Input and try again.",'bred')
                continue
            if index==100:
                cprint("Quit the whole test.",'bblue')
                # sys.exit()
                return
            if index >4 or index<0:
                cprint("Out of range, please try again.",'bred')
                continue
            m=json.dumps(msg[index]).encode()
            s.send(m)
            #time.sleep(15)

    def worker_recv(self,conn):
        while True:
            recv=conn.recv(1024)
            d=par_msg(recv)
            print("Type:{},Content:{}".format(cprint(d['type'],'yellow',False),cprint(d['content'],'green',False)))

    def run(self):
        self.s.listen(self.links)
        flag=True
        while True:
            conn,addr=self.s.accept()
            cprint("A work {} is connected.".format(cprint(addr,'yellow',False)))
            r=conn.recv(1024)
            d=par_msg(r)
            if d['type']=='register':
                print("Message Recv: {}".format(cprint(r.decode(),'blue',False)))
                conn.send("success".encode())
                addr=(d['content']['ip'],d['content']['port'])
                cprint("Try to send a hello world to the worker...",'bblue')
                self.tester(addr)
            
                # if flag==True:
                #     p=Process(target=self.tester,args=(addr,))
                #     p.daemon=True
                #     p.start()
                #     flag=False
                    # cprint("Tester is running...",'green')
                    # p2=Process(target=self.worker_recv,args=(conn,))
                    # p2.daemon=True
                    # p2.start()

            else:
                pass
            
            
                



if __name__ == '__main__':
    s=server(("localhost",60001))
    s.run()

    





