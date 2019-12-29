import sys
#import numpy as np
from NormalizeData import GetMaxCoverData
from random import randint

def Sample(orginData,sampleNum):
    length=len(orginData)
    t=0
    dataFile=open('Sample.txt','w')
    while t<sampleNum:
        index=randint(0,length-1)
        for item in orginData[index]:
            dataFile.write('%d '%(item))
        dataFile.write('\n')    
        del orginData[index]
        length-=1
        t+=1    
    dataFile.close()
    
    
if __name__=="__main__":
    print("start")
    orginX,itemNum=GetMaxCoverData("../data/accident.txt")#the notation begins from 1
    Sample(orginX,10000)
        
