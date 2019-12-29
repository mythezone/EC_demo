import pygame,sys,json,sqlite3,time,random
from pygame.locals import QUIT,MOUSEBUTTONUP,BUTTON_WHEELUP,BUTTON_WHEELDOWN

#pygame.init()

WHITE=(255,255,255)
B_GREY=(50,50,50)
BLACK=(0,0,0)
SITE=(255,0,0)
PORT=(255,255,0)
LOCK=(177,0,0)
OVER=(199,199,199)
Colors=[(128,128,0),(0,128,128),(0,128,0),(128,0,128),(0,0,128),(128,0,0),(45,72,88),(93,172,44),(80,23,0)]
Colors_site=[(192,192,0),(0,192,192),(0,192,0),(192,0,192),(0,0,192),(192,0,0),(45,72,88),(93,172,44),(80,23,0)]


# def generate_result(num,max_t=1000,record=100,population=5):
#     results=[]
#     candidates=[i for i in range(record)]
#     for _ in range(num):
#         test_data={
#                     "time":time.time(),
#                     "iteration":random.randint(1,max_t),
#                     "fitness":random.randint(50,99),
#                     "individual": [random.choice(candidates) for _ in range(population)],
#                     "finger":[random.randint(0,2**450) for _ in range(population)]
#                 }

#         results.append(test_data)
#     return results

def set_text(center,text,anti=True,color=WHITE,size=60,family='freesansbold.ttf'):
    title=pygame.font.Font(family,size)
    titleSObj=title.render(text,anti,color)
    titleRect=titleSObj.get_rect()
    titleRect.left=center[0]
    titleRect.top=center[1]
    return titleSObj,titleRect

def draw_text(center,text,anti=True,color=BLACK,size=60,family='freesansbold.ttf',s=None):
    res,res_r=set_text(center,text,anti,color,size,family)
    s.blit(res,res_r)

def draw_board(rs,s):
    s.fill(WHITE)
    for r in rs:
        pygame.draw.rect(s,B_GREY,r)

class Visualization:
    def __init__(self,data,max_boxes):
        pygame.init()
        self.screen=pygame.display.set_mode((1020,1020))
        pygame.display.set_caption("Evolution Display")
        self.fpsClock=pygame.time.Clock()
        self.data=data
        self.board=pygame.Rect(0,200,1020,820)
        self.max_boxes=max_boxes
        self.get_boxes()

    def updateData(self,data):
        self.data=data

    def draw_info(self):
        draw_text((20,20),"Best Individual",size=50,s=self.screen)
        draw_text((20,75),"Time cost : ",size=30,s=self.screen)
        draw_text((180,75),"%4.1f"%self.data['time'],size=30,s=self.screen)
        draw_text((20,110),"Fitness :",size=30,s=self.screen)
        draw_text((180,110),"%d"%self.data['fitness'],size=30,s=self.screen)
        draw_text((20,145),"Solution :",size=30,s=self.screen)
        solution=self.data['individual']
        for i in range(len(solution)):
            draw_text((180+120*i,145),'%s'%solution[i],size=30,color=Colors_site[i],s=self.screen)

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

    def draw_boxes(self):
        for i in range(len(self.set)):
            boxes=self.set[i]
            for box in boxes:
                r=self.boxes[box]
                pygame.draw.rect(self.screen,Colors_site[i],r)

    def get_boxes(self):
        self.boxes=[]
        for i in range(self.max_boxes):
            tmp=pygame.Rect(10+i%25*40+2,210+i//25*40+1,36,36)
            self.boxes.append(tmp)
        return

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.display.quit()
                    quit()
                    sys.exit()
                    return 
                elif event.type==MOUSEBUTTONUP:
                    quit()
                    sys.exit()
                    return
            draw_board(self.boxes,self.screen)
            self.draw_info()
            self.get_indexes()
            self.draw_boxes()
            pygame.display.update()
            self.fpsClock.tick(30)

if __name__ == '__main__':
    d=generate_result(1,max_t=2000,record=450,population=5)[0]
    v=Visualization(d,450)
    v.run()

