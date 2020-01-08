import sys,random,time,json,copy,socket
from re import split
import numpy as np 
from math import exp,ceil,log
from multiprocessing import Process,Queue,Lock,Manager


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

def opt(dataSet,k):
    m=len(dataSet)
    #init_solution=sorted([random.randint(0,m) for _ in range(k)])
    init_solution=[]
    population=[(init_solution,objectivevalue(init_solution,dataSet))]
    t=0
    T=int(ceil(m*k*k*2*exp(1)))
    iter1=0
    while t<100:
        iter1+=1
        if iter1%(k*m)==0:
            iter1=0
            choose_best(population,k)
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
    p=choose_best(population,k,r=True)
    return p


class listener(Process):
    def __init__(self,addr,master_addr):
        Process.__init__(self)
        self.addr=addr
        self.master_addr=master_addr
        self.s=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)


def message_generator(tp,dct):
    msg={
        'type':tp,
        'content':dct
    }
    return json.dumps(msg).encode()

def message_parser(msg):
    m=json.loads(msg.decode())
    return m


if __name__ == '__main__':
    start=time.time()
    print("My Poss start:")
    d=getData('accident.txt',save_json=True)
    #d=get_json_data('accident.json')
    data_time=time.time()
    print("Read data time : ",data_time-start)
    res=opt(d,5)
    print(res)
    end=time.time()
    print("total time is :",end-data_time)

    
