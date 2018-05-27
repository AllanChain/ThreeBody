import pygame,time,os
from random import random
from pygame.locals import *
from vector import *
SCREENX,SCREENY=500,500
DISPLAY=pygame.display.set_mode((SCREENX,SCREENY))
D=30
G=100
DT=0.1
KEY_MAP={K_DOWN:V3(0,0,1),
         K_UP:V3(0,0,-1),}
class Star:
    def __init__(self,m,v,p):
        self.m=m
        self.v=v
        self.p=p
        return
    def setv(self,s1,s2):
        a=(s1.m*(s1.p-self.p)/(s1.p-self.p).dis**3+\
                 s2.m*(s2.p-self.p)/(s2.p-self.p).dis**3)*G
        #print(a.x,a.y,a.z)
        self.v+=a*DT
        #print(self.p.x,self.p.y,self.p.z)
        self.p+=self.v
        #print(self.p.x,self.p.y,self.p.z)
        #print('_'*20)
    def __str__(self):
        return("position:(%d,%d,%d)\nvelocity:(%d,%d,%d)\n"\
               %(self.p.x,self.p.y,self.p.z,self.v.x,self.v.y,self.v.z)\
               +"screen_position:(%d,%d)"%get_screen_pos(self.p))
class StarGroup:
    def __init__(self,stars,dis):
        self.stars=stars
        self.display=dis
    def proceed(self):
        self.stars[0].setv(self.stars[1],self.stars[2])
        self.stars[1].setv(self.stars[0],self.stars[2])
        self.stars[2].setv(self.stars[1],self.stars[0])
    def draw(self):
        DISPLAY.fill((0,0,0))
        for star in self.stars:
            screen_pos=get_screen_pos(star.p)   
            if star.p.z>0:
                pygame.draw.circle(DISPLAY,(0,0,255),screen_pos,int(D/star.p.z/2))
        pygame.display.update()
    def add(self,vec):
        for star in self.stars:
            star.p+=vec
    def __str__(self):
        info='='*20+'\n'
        for star in self.stars:
            info+=str(star)+'\n'+'-'*20+'\n'
        return info
def ranpro():
    return(V3(random()*2-1,random()*2-1,random()*2-1))
def get_screen_pos(p):
    x,y=p.getv2(D)
    x+=SCREENX//2
    y+=SCREENY//2
    return (x,y)
def main():
    global D,STARS
    while True:
        time.sleep(0.1)
        STARS.proceed()
        STARS.draw()
        if random()<0.2:
            print(STARS)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                os._exit(0)
            if event.type==KEYDOWN:
                vec=KEY_MAP.get(event.key,None)
                if vec!=None:
                    STARS.add(vec)
                    #print('done')
                elif event.key==K_RETURN:
                    return
while True:
    s1=Star(1,ranpro()/10,ranpro()*5+V3(0,0,5))
    s2=Star(1,ranpro()/10,ranpro()*5+V3(0,0,5))
    s3=Star(1,V3(0,0,0)-s1.m*s1.v-s2.m*s2.v,V3(0,0,20)-s1.m*s1.p-s2.m*s2.p)
    STARS=StarGroup((s1,s2,s3),DISPLAY)
    print('here')
    main()
