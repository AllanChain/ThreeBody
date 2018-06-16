import math
class V2:
    def __init__(self,x,y):
          self.x=x
          self.y=y
          self.dis=math.sqrt(self.x*self.x+self.y*self.y)
    def __add__(self,vec):
        return V2(self.x+vec.x,self.y+vec.y)
    def __sub__(self,vec):
        return V2(self.x-vec.x,self.y-vec.y)
    def __mul__(self,n):
        return V2(self.x*n,self.y*n)
    def __floordiv__(self,n):
        return V2(self.x//n,self.y//n)
    def __truediv__(self,n):
        return V2(self.x/n,self.y/n)
    def normalize(self):
        self.x/=self.dis
        self.y/=self.dis

class V3:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        self.square=x**2+y**2+z**2
        self.dis=math.sqrt(self.square)
    def __add__(self,vec):
        return V3(self.x+vec.x,self.y+vec.y,self.z+vec.z)
    def __radd__(self,vec):
        return V3(self.x+vec.x,self.y+vec.y,self.z+vec.z)
    def __sub__(self,vec):
        return V3(self.x-vec.x,self.y-vec.y,self.z-vec.z)
    def __mul__(self,n):
        return V3(self.x*n,self.y*n,self.z*n)
    def __rmul__(self,n):
        return V3(self.x*n,self.y*n,self.z*n)
    def __floordiv__(self,n):
        return V3(self.x//n,self.y//n,self.z//n)
    def __truediv__(self,n):
        return V3(self.x/n,self.y/n,self.z/n)
    def __format__(self,f):
        return f'({self.x:{f}},{self.y:{f}},{self.z:{f}})'
    def normalize(self):
        self.x/=self.dis
        self.y/=self.dis
        self.z/=self.dis
        self.dis=self.square=1
    def getv2(self,d):
        return (int(self.x*d/self.z),int(self.y*d/self.z))

