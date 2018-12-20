## Imagination Machine 2.0 by Clara Leivas, 2018 
## licensed under CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/

class plot:
    # -*- coding: utf-8 -*-
    ps = 0
    mi = 3000000
    ma = 7000000
    preX = 0
    preY = 0
    
    def __init__(self, plotterserial):
        self.ps = plotterserial
        #for i in range(self.nFD):
         #   self.dif[i] = 0
        
    def draw(self, _x, _y, _o, _p, _b):
        xMax = 200
        yMax = 200
        print("x")
        print(_x)
        print("y")
        print(_y)
        
        x = self.mapR(_x, self.mi, self.ma, 0, xMax)
        x = self.constrain(x, 0, xMax)
        y = self.mapR(_y, self.mi, self.ma, 0, yMax)
        y = self.constrain(y, 0, yMax)
        
        print("x")
        print(x)
        print("y")
        print(y)
        
        self.goTo(x, y)
        self.preX = x
        self.preY = y
        
    def goTo(self, _x, _y):
        x = _x
        y = _y
        send = "x" + str(x) +" y" + str(y) + "\r\n"
        self.ps.write(send.encode())
    
    def reset(self):
        self.goTo(0, 0)
    
    def mapR(self, x, in_min, in_max, out_min, out_max):
      return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
  
    def constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))
    


        
