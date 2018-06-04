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
gravity_dict={0:(1,2),
                  1:(0,2),
                  2:(0,1)}
class Star:
    def __init__(self,m,v,p):
        self.m=m
        self.v=v
##        self.p=p
        self._p=[p,p+v*DT]
        a=[self.calc_a]
        return
    @property
    def p(self):
        return self._p[1]
    def calc_a(self,s1,s2):
        self.a=(s1.m*(s1.p-self.p)/(s1.p-self.p).dis**3+\
                 s2.m*(s2.p-self.p)/(s2.p-self.p).dis**3)*G
        return self.a
    def proceed(self,s1,s2):
        self._p.append(2*self.p-self._p.pop(0)+self.a*DT**2)
        #print(a.x,a.y,a.z)
        self.v+=(self.a+self.calc_a(s1,s2))/2*DT
        #print(self.p.x,self.p.y,self.p.z)
        #self.p+=self.v*DT
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
        self.M=0
        for star in stars:
            self.M+=star.m
    def calc_rc(self):
        r=v=V3(0,0,0)
        E=0
        for i,j in gravity_dict.items():
            E+=1/2*self.stars[i].m*self.stars[i].v.dis**2
            E-=G*self.stars[j[0]].m*self.stars[j[1]].m\
                /(self.stars[j[0]].p-self.stars[j[1]].p).dis
            r+=self.stars[i].p
            v+=self.stars[i].v
##        for star in self.stars:
##            r+=star.p
##            v+=star.v
##            E+=1/2*star.m*star.v.dis**2
##        for i,j in ((0,1),(1,2),(0,2)):
##            E-=G*self.stars[i].m*self.stars[j].m/(self.stars[i].p-self.stars[j].p).dis
        return r/self.M,v/self.M,E
    def proceed(self):
        for i,j in gravity_dict.items():
            self.stars[i].calc_a(self.stars[j[0]],self.stars[j[1]])
        for i,j in gravity_dict.items():
            self.stars[i].proceed(self.stars[j[0]],self.stars[j[1]])

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
        rc,vc,E=self.calc_rc()
        info+='rc:(%d,%d,%d),vc:(%d,%d,%d)'%(rc.x,rc.y,rc.z,vc.x,vc.y,vc.z)
        info+='\nEnergy:'+str(E)
        return info
def ranpro():
    return(V3(random()*2-1,random()*2-1,random()*2-1))
def random_star():
    s1=Star(1,ranpro()/10,ranpro()*5+V3(0,0,5))
    s2=Star(1,ranpro()/10,ranpro()*5+V3(0,0,5))
    s3=Star(1,V3(0,0,0)-s1.m*s1.v-s2.m*s2.v,V3(0,0,20)-s1.m*s1.p-s2.m*s2.p)
    return StarGroup((s1,s2,s3),DISPLAY)

def get_screen_pos(p):
    x,y=p.getv2(D)
    x+=SCREENX//2
    y+=SCREENY//2
    return (x,y)
def main():
    global D,STARS
    STARS=random_star()
    while True:
        time.sleep(0.1)
        STARS.proceed()
        STARS.draw()
        if random()<0.8:
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
                    print('*'*10+'NEW'+'*'*10)
                    STARS=random_star()
main()
