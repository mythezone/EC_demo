#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Mythezone
# DATE: 2019/12/23 Mon
# TIME: 00:25:18

# DESCRIPTION: A server

import socket,sys,time,json,random,copy,os,argparse
from multiprocessing import Process,Manager,Lock,Queue
from utils import cprint
from message import reg_msg,par_msg,gen_msg
from math import exp,ceil,log
from re import split

def getData(filepath,lens=None,save_json=False):
    datalist=[]
    with open(filepath,'r') as f:
        lines=f.readlines()
        if lens==None:
            for line in lines[:]:
                #print(line)
                lineArray=split(r'\s+',line)
                lineArray = filter(lambda x: x !='', lineArray)
                finger=0
                for i in lineArray:
                    finger+=2**int(i)
                datalist.append(finger)
        else:
            for line in lines[:lens]:
                #print(line)
                lineArray=split(r'\s+',line)
                lineArray = filter(lambda x: x !='', lineArray)
                finger=0
                for i in lineArray:
                    finger+=2**int(i)
                datalist.append(finger)
    #print(datalist)
    if save_json==True:
        with open('accident.json','w') as f:
            f.write(json.dumps(datalist))
    return datalist

def get_json_data(filepath):
    with open(filepath,'r') as f:
        d=json.loads(f.read())
    return d

def finger_len(finger):
    l=0
    while finger!=0:
        l+=finger%2
        finger//=2
    return l
  
def mutation(s1,n):
    solution=copy.deepcopy(s1)
    k=1.0/n
    for i in range(n):
        if random.random()<k:
            if i in solution:
                solution.remove(i)
            else:
                solution.append(i)
    return solution

def objectivevalue(solution,dataSet):
    finger=0
    for s in solution:
        finger=finger|dataSet[s]
    return finger_len(finger)

def choose_best(population,k,r=False):
    result=None
    maxSize=-1
    for p in population:
        if len(p[0])<=k and p[1]>maxSize:
            maxSize=p[1]
            result=p
    print('Best Solution now is :',result)
    if r==True:
        return result

def set_mid_result(dct):
    for key,value in dct.items():
        mid_result[key]=value

def init_mid_result():
    set_mid_result({        
    "solution":[],
    "fitness":0,
    "iteration":0,
    "timecost":0,
    "final":False,})

def get_final_statu():
    print("Check:",mid_result)
    if mid_result['final']==True:
        cprint("Final",'bred')
        return True
    else:
        cprint("Result",'bgreen')
        return False

def opt(dataSet,population_in,iteration=10000,k=5):
    time_start=time.time()
    m=len(dataSet)
    #init_solution=sorted([random.randint(0,m) for _ in range(k)])
    #init_solution=[]
    population=[(p,objectivevalue(p,dataSet)) for p in population_in]
    population.insert(0,([],0))
    t=0
    T=iteration#int(ceil(m*k*k*2*exp(1)))
    iter1=0
    while t<T:
        iter1+=1
        # if iter1%(k*m)==0:
        if iter1%25==0:
            iter1=0
            tmp=choose_best(population,k,r=True)
            tmp_result={
                "solution":tmp[0],
                "fitness":tmp[1],
                "iteration":t,
                "timecost":time.time()-time_start
            }
            set_mid_result(tmp_result)
            print("mid_result:",tmp_result)
            # resultIndex=-1
            # maxSize=-1
            # for p in population:
            #     if len(p[0])<=k and p[1]>maxSize:
            #         maxSize=p[1]
            #         resultIndex=p
            # print('Best Solution now is :',population[resultIndex])
        s=random.choice(population)
        offSpring_solution=mutation(s[0],m)
        lo=len(offSpring_solution)
        if lo==0 or lo>=2*k:
            tmp_f=0
        else:
            tmp_f=objectivevalue(offSpring_solution,dataSet)
        #print(tmp_f)
        offSpring=(offSpring_solution,tmp_f)
        hasBetter=False
        fo=offSpring[1]
        lo=len(offSpring[0])
        for s in population:
            ls=len(s[0])
            fs=s[1]
            if (fs>fo and ls<=lo) or (fs>=fo and ls<lo):
                hasBetter=True
                break
        if hasBetter==False:
            Q=[]
            for s in population:
                ls=len(s[0])
                fs=s[1]
                if fo>=fs and lo<=ls:
                    continue
                else:
                    Q.append(s)
            population=Q
            population.append(offSpring)

        t+=1
    tmp=choose_best(population,k,r=True)
    tmp_result={
                "solution":tmp[0],
                "fitness":tmp[1],
                "iteration":t,
                "timecost":time.time()-time_start,
                "final":True
            }
    set_mid_result(tmp_result)
    print(tmp_result)
    return tmp_result

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
        self.data_path='accident.txt'
        self.dataSet=[]
        self.final=False
        self.send_list=Queue()
        self.t=None
        # self.result=Manager().dict()
        print(self.dataSet[:2])
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

    # def get_message_sender(self):
    #     s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #     s.connect(self.master)
    #     return s
    
    def sender(self,msg,clsd=True):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(self.master)
        s.send(msg)
        if clsd:
            s.close()
        else:
            s.shutdown(1)


    def set_dataSet(self):
        self.dataSet=getData(self.data_path)

    def register(self,idin=None):
        msg=reg_msg(self.myaddr,idin)
        # s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        count=0
        
        while True:
            try:
                # s.connect(self.master)
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                cprint("Start to connect the master server...",'blue')
                s.connect(self.master)
                cprint("Try to send a register message:",'blue')
                s.send(msg)
                s.shutdown(1)
                cprint("Try to recv a response from the master server:",'blue')
                r=s.recv(1024)
                tmp=cprint("RECV: ",'blue',False)
                
                print("{}{}".format(tmp,cprint(r.decode(),'green',False)))
                return
            except:
                cprint("Connect failed, try to connect after 2 seconds.",'red')
                count+=1
                if count==5:
                    cprint("Error: Cannot connect to the master, please check if the server is running.",'bred')
                    sys.exit()
                time.sleep(2)
                continue
        cprint("Linked success!!",'green')

    def algorithm_run(self,population,iteration,k,idin):
        self.set_dataSet()
        res=opt(self.dataSet,population,iteration,k)
        cprint(res,'green')
        msg=gen_msg('final',idin,res)
        cprint("Final:"+msg.decode(),'bred')
        

    def msg_handler(self,recv,conn):
        msg=json.loads(recv)
        tp,idin,content=msg['type'],msg['id'],msg['content']
        if tp=='file':
            re_msg=gen_msg('comment',idin,{'status':"succeed",'msg':"success to download file."})
            conn.send(re_msg)
            conn.close()
            try:
                if self.data_path==None or self.data_path!=content['url']:
                    self.data_path=content['url']
                    _data_md5=content['md5']
                    # downloading file and check the md5
                    cprint("md5:{}".format(_data_md5),'green')
                    self.set_dataSet()
                else:
                    cprint("File aready exist.",'yellow')
            except:
                pass

        elif tp=='start':
            population=content['population']
            iteration=content['iteration']
            k=content['k']
            re_msg=gen_msg('started',idin,{})
            conn.send(re_msg)
            conn.close()
            init_mid_result()
            self.t=Process(target=self.algorithm_run,args=(population,iteration,k,idin))
            cprint("Algorithm started...",'bblue')
            self.t.start()

        elif tp=='stop':
            self.t.terminate()
            while self.t.is_alive():
                time.sleep(0.5)
            cprint("Stopped by Master.",'bred')
            msg=gen_msg('stopped',idin,mid_result)
            conn.send(msg)
            conn.close()

        elif tp=='query':
            if get_final_statu():
                rtp='final'
            else:
                rtp='result'
            cprint("Response:"+rtp,'blue')
            msg=gen_msg(rtp,idin,mid_result)
            conn.send(msg)
            conn.close()

        elif tp=='comment':
            print("Recv Comment:{}".format(cprint(content['msg'],'green',False)))

        else:
            cprint("This type of message is not supported yeat,please check.",'bred')
            cprint("Message Type:{}".format(tp),'red')


    def run(self):
        self.s.listen(self.links)
        while True:
            conn,addr=self.s.accept()
            print("A connection recv from:{}".format(cprint(addr,'yellow',False)))
            recv=conn.recv(1024)
            print("{}{}".format(cprint("Recv:",'blue',False),cprint(recv.decode(),'green',False)))
            # msg=par_msg(recv)
            self.msg_handler(recv,conn)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',type=str,default='localhost')
    parser.add_argument('--port',type=int,default=64001)
    parser.add_argument('--masterhost',type=str,default='localhost')
    parser.add_argument('--masterport',type=int,default=60001)
    args=parser.parse_args()

    s=server((args.host,args.port),("10.17.62.150",9999))
    
    mid_result=Manager().dict({        
        "solution":[],
        "fitness":0,
        "iteration":0,
        "timecost":0,
        "final":False,
    })
    s.start()
    while True:
        time.sleep(10)
        cprint("Mid Result:{}".format(mid_result),'yellow')