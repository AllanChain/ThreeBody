import time,os
from random import random
from vector import *
try:
    import pygame
    from pygame.locals import *
    WINDOW=True
except ImportError:
    WINDOW=False

DISPLAY=None
SCREENX,SCREENY=500,500
D=30 #视距
G=100 #引力常量
DT=0.01 #每次循环三体的时间差Δt
WAIT=0.05 #每次pygame循环现实中经历时间
WAIT_C=0.1 #每次命令行循环现实中经历时间
#储存相互作用方式的字典
gravity_dict={0:(1,2),
                1:(0,2),
                2:(0,1)}
class Star:
    def __init__(self,m,v,p):
        self.m=m
        self.v=v
        #计算t=0,Δt的位置
        self._p=[p,p+v*DT]

        #计算t=0时刻的加速度
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
        self.v+=(self.a+self.calc_a(s1,s2))/2*DT
    def __str__(self):
        return(
        f'''position:{self.p:.2f}
velocity:{self.v:.2f}
screen_position:{get_screen_pos(self.p)}''')
class StarGroup:
    
    def __init__(self,stars,dis=None):
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
                r=max(int(D/star.p.z/2),3)
                pygame.draw.circle(DISPLAY,(0,0,255),screen_pos,r)
        pygame.display.update()
    def add(self,vec):
        for star in self.stars:
            star.p+=vec
    def __str__(self):
        info='='*20+'\n'
        for star in self.stars:
            info+=str(star)+'\n'+'-'*20+'\n'
        rc,vc,E=self.calc_rc()
        info+=f'rc:{rc:.0f},vc:{vc:.0f}'
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
def main_in_pygame():
    global D,STARS,DISPLAY
    #按下相应键的坐标增减
    KEY_MAP={K_DOWN:V3(0,0,1),
                K_UP:V3(0,0,-1),}
    PRINT_FEQ=0.2 #输出信息的频率
    DISPLAY=pygame.display.set_mode((SCREENX,SCREENY))
    STARS=random_star()
    while True:
        time.sleep(WAIT)
        STARS.proceed()
        STARS.draw()
        if random()<PRINT_FEQ:
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
def main_in_console():
    global D,STARS
    
    STARS=random_star()
    while True:
        try:
            time.sleep(WAIT_C)
            STARS.proceed()
            print(STARS)
        except KeyboardInterrupt:
            if input('Again?'):
                print('*'*10+'NEW'+'*'*10)
                STARS=random_star()
            else:
                return
if WINDOW==False:           
    main_in_console()
else:
    main_in_pygame()
