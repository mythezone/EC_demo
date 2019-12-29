import matplotlib.pyplot as plt 
#from matplotlib.pyplot import 
from matplotlib.patches import Rectangle
import time,random
from mpl_toolkits.mplot3d import Axes3D

WHITE=(255,255,255)
B_GREY=(50,50,50)
BLACK=(0,0,0)
SITE=(255,0,0)
PORT=(255,255,0)
LOCK=(177,0,0)
OVER=(199,199,199)
Colors=['lightcoral','olive','deepskyblue','darkorchid','royalblue','green','lightslategrey']
Colors_site=[(192,192,0),(0,192,192),(0,192,0),(192,0,192),(0,0,192),(192,0,0),(45,72,88),(93,172,44),(80,23,0)]

def test_visual():
    fig,ax=plt.subplots(subplot_kw={"aspect":"equal"})

    rectangle=ax.patch
    rectangle1=Rectangle((1,0),3,3,facecolor='lightskyblue',edgecolor='rosybrown')
    ax.add_patch(rectangle1)

    ax.axis([0,5,0,6])

    plt.show()

def generate_result(num,max_t=1000,record=100,population=5):
    results=[]
    candidates=[i for i in range(record)]
    for _ in range(num):
        test_data={
                    "time":time.time(),
                    "iteration":random.randint(1,max_t),
                    "fitness":random.randint(50,99),
                    "individual": [random.choice(candidates) for _ in range(population)],
                    "finger":[random.randint(0,2**450) for _ in range(population)]
                }

        results.append(test_data)
    return results

class show_visual:
    def __init__(self,data,max_boxes):
        self.data=data
        self.max_boxes=max_boxes
        fig,self.ax=plt.subplots(subplot_kw={"aspect":"equal"})
        self.rectangle=self.ax.patch
        self.ax.axis([0,25,0,20])
        self.get_indexes()

    def finger_to_int(self,finger):
        res=[]
        s=bin(finger)[2:]
        s=s[::-1]
        l=len(s)
        for i in range(l):
            if s[i]=='1':
                res.append(i)
        return res

    def get_indexes(self):
        self.set=[]
        fingers=self.data['finger']
        for finger in fingers:
            tmp=self.finger_to_int(finger)
            self.set.append(tmp)

    def get_boxes(self):
        self.boxes=[]
        for i in range(self.max_boxes):
            tmp=Rectangle((i%25,i//25),1,1,facecolor='w',edgecolor='black')
            self.boxes.append(tmp)

    def draw_boxes(self):
        for i in range(len(self.set)):
            boxes=self.set[i]
            for box in boxes:
                self.boxes[box]=Rectangle((box%25,box//25),1,1,facecolor=Colors[i],edgecolor='black')
                #r.facecolor='red'

    def show(self):
        self.get_boxes()
        self.draw_boxes()

        for b in self.boxes:
            self.ax.add_patch(b)
        plt.show()

def finger_to_int(finger):
        res=[]
        s=bin(finger)[2:]
        s=s[::-1]
        l=len(s)
        for i in range(l):
            if s[i]=='1':
                res.append(i)
        return res

def get_indexes(data):
    my_set=[]
    fingers=data['finger']
    for finger in fingers:
        tmp=finger_to_int(finger)
        my_set.append(tmp)
    return my_set

def get_boxes(max_boxes):
    boxes=[]
    for i in range(max_boxes):
        tmp=Rectangle((i%25,i//25),1,1,facecolor='w',edgecolor='black')
        boxes.append(tmp)
    return boxes

def draw_boxes(my_set,res_boxes):
    for i in range(len(my_set)):
        boxes=my_set[i]
        for box in boxes:
            res_boxes[box]=Rectangle((box%25,box//25),1,1,facecolor=Colors[i],edgecolor='black')
    return res_boxes

def draw_individual(d,max_boxes):
    fig,ax=plt.subplots(subplot_kw={"aspect":"equal"})
    rectangle=ax.patch
    ax.axis([0,25,0,20])
    boxes=get_boxes(max_boxes)
    myset=get_indexes(d)
    boxes=draw_boxes(myset,boxes)
    for box in boxes:
        ax.add_patch(box)
    plt.show()

def get_ax(d,max_boxes):
    fig,ax=plt.subplots(subplot_kw={"aspect":"equal"})
    rectangle=ax.patch
    ax.axis([0,25,0,20])
    boxes=get_boxes(max_boxes)
    myset=get_indexes(d)
    boxes=draw_boxes(myset,boxes)
    for box in boxes:
        ax.add_patch(box)
    return ax

def show_3d(ds,max_boxes):
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1,projection='3d')

    for i in range(len(ds)):
        d=ds[i]
        bx=get_ax(d,max_boxes)
        



if __name__ == '__main__':
    d=generate_result(5)[0]
    draw_individual(d,500)

        