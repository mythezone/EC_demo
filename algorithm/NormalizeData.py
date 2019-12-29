#this code is to standardize the variable to get mean 0 and variance 1.
#python version is 2.7
import sys
from re import split
import numpy as np
from math import exp
def NormlizeDateSpareseRegression(filepath):
    try:
        myfile=open(filepath)
        lines = myfile.readlines()
        dataMatrix=[]
        for line in lines:
            lineArray=split(r'\s+',line)
            lineArray = filter(lambda x: x !='', lineArray)
            dataMatrix.append(lineArray)
        dataMatrix=np.mat(dataMatrix,dtype="float64")
        matSize=np.shape(dataMatrix)
        for i in range(0,matSize[1]):
            theColum=dataMatrix[:,i]
            columnMean=sum(theColum)/matSize[0]
            minusColumn=np.mat(theColum-columnMean)
            std=np.sqrt(np.transpose(minusColumn)*minusColumn/matSize[0])
            dataMatrix[:,i]=(theColum-columnMean)/std
            '''
        normDateFile=open('housingNormdata.txt','w')
        for i in range(0,matSize[0]):
            for j in range(0,matSize[1]):
                normDateFile.write("%f "%dataMatrix[i,j])
            normDateFile.write("\n")
           ''' 
        return dataMatrix
    except  Exception as e:
        print  (e)
    finally:
        myfile.close()
        #normDateFile.close()
     
     
def NormlizeDateActiveSetSelection(filepath):
    try:
        myfile=open(filepath)
        lines = myfile.readlines()
        dataMatrix=[]
        for line in lines:
            lineArray=split(r'\s+',line)
            lineArray = filter(lambda x: x !='', lineArray)
            dataMatrix.append(lineArray)
        dataMatrix=np.mat(dataMatrix,dtype="float64")
        [m,n]=np.shape(dataMatrix)
        for i in range(0,m):
            theRow=dataMatrix[i,:]
            rowMean=sum(theRow)/n
            minusColumn=np.mat(theRow-rowMean)
            std=np.sqrt(minusColumn*np.transpose(minusColumn)/n)
            dataMatrix[i,:]=(theRow-rowMean)/std
        '''
        normDateFile=open('parkNormdata.txt','w')
        for i in range(0,m):
            for j in range(0,n):
                normDateFile.write("%f "%dataMatrix[i,j])
            normDateFile.write("\n")
        ''' 
        return dataMatrix
    except  Exception as e:
        print  (e)
    finally:
        myfile.close()
        #normDateFile.close()
    


def GetMaxCoverData(filepath):
    try:
        myfile=open(filepath)
        lines = myfile.readlines()
        dataMatrix=[]
        maxNum=0
        for line in lines:
            lineArray=split(r'\s+',line)
            lineArray = filter(lambda x: x !='', lineArray)
            temp=[]#[int(item) for item in lineArray]
            for item in lineArray:
                tempnum=int(item)
                if maxNum<tempnum:
                    maxNum=tempnum
                temp.append(tempnum)
            dataMatrix.append(temp)   
        '''
        normDateFile=open('parkNormdata.txt','w')
        for i in range(0,m):
            for j in range(0,n):
                normDateFile.write("%f "%dataMatrix[i,j])
            normDateFile.write("\n")
        ''' 
        return (dataMatrix,maxNum)
    except  Exception as e:
        print  (e)
    finally:
        myfile.close()
        #normDateFile.close()        

if __name__=="__main__":
    #NormlizeDateSpareseRegression('housing.txt')
    X,num=GetMaxCoverData('../housing.txt')
    print( len(X),num)
    #[m,n]=np.shape(X)#row and column number of the matrix
    '''
    for i in range(0,m):
        for j in range(i,m):
            tempvector=X[i,:]-X[j,:]
            #Sigma[i,j]=exp(0-((tempvector*tempvector.T)/0.5625))
            print 0-(tempvector*tempvector.T)/0.5625
        
            Sigma[j,i]=Sigma[i,j]
    normDateFile=open('Sigma_housing.txt','w')
    for i in range(0,m):
        for j in range(0,m):
            normDateFile.write("%f "%Sigma[i,j])
        normDateFile.write("\n")   
        '''   