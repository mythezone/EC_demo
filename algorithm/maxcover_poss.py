# the python version is 2.7
import sys,time
import numpy as np
from random import randint
from math import ceil
from math import exp
from math import log
from NormalizeData import GetMaxCoverData
from copy import deepcopy

class ParetoOpt:
    def mutation(self,s,n):#every bit will be flipped with probability 1/n
        s_temp=deepcopy(s)
        for i in range(1,n+1):
            if randint(1,n)==i:#the probability is 1/n
                s_temp[0,i-1]=(s[0,i-1]+1)%2
        return s_temp

    def position(self,s,n):#This function is to find the index of s where element is 1
        #n=np.shape(s)[1]
        result=[]
        for i in range(0,n):
            if s[0,i]==1:
                result.append(i)
        return result   
    
    
    def objectivevalue(self,s,itemNum,n):#itemNum record the number of the universal set
        indexs=self.position(s,n)
        flag=np.mat(np.zeros([1,itemNum]),'int8')
        for i in indexs:
            temparr=self.set[i]
            for j in temparr:
                flag[0,j-1]=1      
        #print flag[0,:].sum()
        return flag[0,:].sum()
                
    def opt(self,X,itemNum,k):
        self.set=X
        m=len(X)#number of subsets
        population=np.mat(np.zeros([1,m],'int8'))#initiate the population
        fitness=np.mat(np.zeros([1,2]))
        fitness[0,0]=0.0
        popSize=1
        t=0#the current iterate count
        T=int(ceil(m*k*k*2*exp(1)))
        iter1=0
        while t<100:
            iter1=iter1+1
            if iter1%(k*m)==0:
                iter1=0
                resultIndex=-1
                maxSize=-1
                for p in range(0,popSize):
                    if fitness[p,1]<=k and fitness[p,1]>maxSize:
                        maxSize=fitness[p,1]
                        resultIndex=p
                print('objective is:%f'%(fitness[resultIndex,0]) )       
            s=population[randint(1, popSize)-1,:]#choose a individual from population randomly
            offSpring=self.mutation(s,m)#every bit will be flipped with probability 1/n
            offSpringFit=np.mat(np.zeros([1,2]))
            offSpringFit[0,1]=offSpring[0,:].sum()
            if offSpringFit[0,1]==0.0 or offSpringFit[0,1]>=2.0*k:
                offSpringFit[0,0]=0.0
            else:
                offSpringFit[0,0]=self.objectivevalue(offSpring,itemNum,m)
            #now we need to update the population
            hasBetter=False    
            for i in range(0,popSize):
                if (fitness[i,0]>offSpringFit[0,0] and fitness[i,1]<=offSpringFit[0,1]) or (fitness[i,0]>=offSpringFit[0,0] and fitness[i,1]<offSpringFit[0,1]):
                    hasBetter=True
                    break
            if hasBetter==False:#there is no better individual than offSpring
                Q=[]
                for j in range(0,popSize):
                    if offSpringFit[0,0]>=fitness[j,0] and offSpringFit[0,1]<=fitness[j,1]:
                        continue
                    else:
                        Q.append(j)
                Q.sort()
                fitness=np.vstack((offSpringFit,fitness[Q,:]))#update fitness
                population=np.vstack((offSpring,population[Q,:]))#update population
                
            t=t+1
            popSize=np.shape(fitness)[0]
        resultIndex=-1
        maxSize=-1 
        for p in range(0,popSize):
            if fitness[p,1]<=k and fitness[p,1]>maxSize:
                maxSize=fitness[p,1]
                resultIndex=p    
        print('objective is:%f'%(fitness[resultIndex,0]) )       
        return population[resultIndex,:]        

    def greedy(self,X,itemNum,k):
        self.set=X
        m=len(X)
        result=np.mat(np.zeros([1,m],'int8'))
        t=0
        finalErr=0
        while t<k:
            index=0
            for i in range(0,m):
                if result[0,i]==0:
                    result[0,i]=1
                    temp=self.objectivevalue(result,itemNum,m)  
                    if finalErr<=temp:
                        finalErr=temp
                        index=i
                    result[0,i]=0
            result[0,index]=1  
            t=t+1  
        print ('objective is:%f'%(finalErr) )
        return result    
        
if __name__=="__main__":
    start=time.time()
    print ("start")
    orginX,itemNum=GetMaxCoverData("data/accident.txt")#the notation begins from 1
    n=np.shape(orginX)[0]
    print ("start algorithm")
    print (len(orginX),itemNum)
    data_time=time.time()
    print("Read data time:",data_time-start)
    paretoopt=ParetoOpt()
    #selectIndex=paretoopt.greedy(orginX,itemNum,5)
    selectIndex=paretoopt.opt(orginX,itemNum,5)
    #print selectIndex
    result=[]
    for i in range(0,n):
        if selectIndex[0,i]==1:
            result.append(i)    
    print (result)
    print ("end")
    end=time.time()
    print("total time is :",end-data_time)
    
   
        
                  
    
