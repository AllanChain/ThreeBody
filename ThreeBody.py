import pygame,time,os
from random import random
from pygame.locals import *
from vector import *
SCREENX,SCREENY=500,500
DISPLAY=pygame.display.set_mode((SCREENX,SCREENY))
D=60
G=0.01
DT=0.1
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
        print(self.p.x,self.p.y,self.p.z)
        self.p+=self.v
        print(self.p.x,self.p.y,self.p.z)
        print('_'*20)
    def __str__(self):
        return("position:(%d,%d,%d)\nvelocity:(%d,%d,%d)\n"\
               %(self.p.x,self.p.y,self.p.z,self.v.x,self.v.y,self.v.z)\
               +"screen_position:(%d,%d)"%get_screen_pos(self.p))
def ranpro():
    return(V3(random()*2-1,random()*2-1,random()*2-1))
def get_screen_pos(p):
    x,y=p.getv2(D)
    x+=SCREENX//2
    y+=SCREENY//2
    return (x,y)
def main():
    global D
    #D=100
    s1=Star(1,ranpro()/5,ranpro()*10+V3(0,0,10))
    s2=Star(1,ranpro()/5,ranpro()*10+V3(0,0,10))
    s3=Star(1,V3(0,0,0)-s1.m*s1.v-s2.m*s2.v,V3(0,0,10)-s1.m*s1.p-s2.m*s2.p)
    for i in (s1,s2,s3):
            print(int(i.p.z))
    time.sleep(0.5)
    s1.setv(s2,s3)
    s2.setv(s1,s3)
    s3.setv(s2,s1)
    DISPLAY.fill((0,0,0))
    print('='*20)
    for i in (s1,s2,s3):
        #print(int(d/i.p.z/2))
        #print(int(i.p.z))
        print(i)
        print('-'*20)
        screen_pos=get_screen_pos(i.p)   
        if i.p.z>0:
            pygame.draw.circle(DISPLAY,(0,0,255),screen_pos,int(D/i.p.z/2))
            pygame.display.update()
    for event in pygame.event.get():
        if event.type==QUIT:
                        pygame.quit()
                        os._exit(0)
        if event.type==KEYDOWN:
                if event.key==K_UP:
                        for i in (s1,s2,s3):
                            i.p.z-=1
                elif event.key==K_DOWN:
                        for i in (s1,s2,s3):
                            i.p.z+=1
##                        if d<=0:
##                                d=0
                elif event.type==K_RETURN:
                        return
while True:
	main()
