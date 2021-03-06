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
PROTECT=2#发生碰撞距离
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
        return
    @property
    def p(self):
        return self._p[1]
    def calc_a(self,s1,s2):
        r1=(s1.p-self.p)
        r2=(s2.p-self.p)
        if r1.dis<PROTECT:
            self.group.crash(self,s1)
        if r2.dis<PROTECT:
            self.group.crash(self,s2)
        self.a=(s1.m*r1/r1.dis**3+\
                 s2.m*r2/r2.dis**3)*G
        return self.a
    def calc_p(self):
        self._p.append(2*self.p-self._p.pop(0)+self.a*DT**2)
    def calc_v(self,s1,s2):
        self.v+=(self.a+self.calc_a(s1,s2))/2*DT
    def __str__(self):
        return(
        f'''position:{self.p:.2f}
velocity:{self.v:.2f}
acceleration:{self.a:.2f}
screen_position:{get_screen_pos(self.p)}''')
class StarGroup:
    def __init__(self,stars,dis=None):
        self.stars=stars
        self.display=dis
        self.M=0
        for star in stars:
            self.M+=star.m
            star.group=self
        for i,j in gravity_dict.items():
            self.stars[i].calc_a(self.stars[j[0]],self.stars[j[1]])
    def calc_rc(self):
        r=v=V3(0,0,0)
        E=0
        for i,j in gravity_dict.items():
            E+=1/2*self.stars[i].m*self.stars[i].v.square
            E-=G*self.stars[j[0]].m*self.stars[j[1]].m\
                /(self.stars[j[0]].p-self.stars[j[1]].p).dis
            r+=self.stars[i].p
            v+=self.stars[i].v
        return r/self.M,v/self.M,E
    def proceed(self):
        for i,j in gravity_dict.items():
            self.stars[i].calc_p()
        for i,j in gravity_dict.items():
            self.stars[i].calc_v(self.stars[j[0]],self.stars[j[1]])
    def crash(self,s1,s2):
        print('#'*10+'CRASH')
        r=s2.p-s1.p
        e=1
        bv=s1.v-s2.v
        if bv.dot(r)>0:
            v1,v2=s1.v,s2.v
            m1,m2=s1.m,s2.m
            v1n=(v1.dot(r)/r.square)*r
            v1t=v1-v1n
            v2n=(v2.dot(r)/r.square)*r
            v2t=v2-v2n
            v1nk=((m1-e*m2)*v1n+(1+e)*m2*v2n)/(m1+m2)
            v2nk=((m2-e*m1)*v2n+(1+e)*m1*v1n)/(m1+m2)
            s1.v=v1nk+v1t
            s2.v=v2nk+v2t
            print(bv)
            print(s1.v-s2.v)
            print(v1n-v2n)
            print(v1nk-v2nk)
            print(1/2*m1*v1.square+1/2*m2*v2.square)
            print(1/2*m1*s1.v.square+1/2*m2*s2.v.square)
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
        if E>0:
            #for i in self.stars:
                #print(i.a)
            print(info)
            raise KeyboardInterrupt
        return info
def ranpro():
    return(V3(random()*2-1,random()*2-1,random()*2-1))
def random_star():
    VMAX=0.1
    s1=Star(1,ranpro()*VMAX,ranpro()*5+V3(0,0,5))
    s2=Star(1,ranpro()*VMAX,ranpro()*5+V3(0,0,5))
    s3=Star(1,V3(0,0,0)-s1.m*s1.v-s2.m*s2.v,V3(0,0,20)-s1.m*s1.p-s2.m*s2.p)
    return StarGroup((s1,s2,s3),DISPLAY)

def get_screen_pos(p):
    x=p.x*D/p.z+SCREENX//2
    y=p.y*D/p.z+SCREENY//2
    return (int(x),int(y))
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
            for i in range(10):
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
