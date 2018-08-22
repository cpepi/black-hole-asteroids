from graphics import *
from math import sin, cos, radians, degrees, sqrt, pi
import random

def distance(obj1, obj2):
    return sqrt((obj1.xpos-obj2.xpos)**2 + (obj1.ypos-obj2.ypos)**2)

def collision(obj1, obj2):
    return True if distance(obj1, obj2) < (obj1.size + obj2.size) else False

class GameObject:

    def __init__(self, win, size, color, angle = (pi)/2, xpos=0, ypos=0):
        self.base = Circle(Point(xpos, ypos), size)
        self.base.setFill(color)
        self.base.setOutline("red")
        self.base.draw(win)
        self.size = size
        self.color = color
        self.win = win
        self.angle = angle
        self.vel = 0.0
        self.xvel = 0.0
        self.yvel = 0.0
        self.ypos = ypos
        self.xpos = xpos

    def update(self, time, bhlist = None):
        if bhlist:
            temp = bhlist[:]
            if self in temp: temp.remove(self)
            for bh in temp:
                dist = distance(self, bh)
                if dist == 0: break
                fgrav = (.6673 * bh.mass * self.mass)/(dist**2)
                self.xvel = self.xvel - fgrav * ((self.xpos-bh.xpos)/dist)
                self.yvel = self.yvel - fgrav * ((self.ypos-bh.ypos)/dist)
        self.xpos = self.xpos + time * self.xvel
        self.ypos = self.ypos + time * self.yvel
        if self.ypos < self.win.trans.ymin:
            self.ypos = self.win.trans.ybase - 1
        if self.ypos > self.win.trans.ybase:
            self.ypos = self.win.trans.ymin + 1
        if self.xpos < self.win.trans.xbase:
            self.xpos = self.win.trans.xmax -1
        if self.xpos > self.win.trans.xmax:
            self.xpos = self.win.trans.xbase + 1
        self.redraw()

    def redraw(self):
        self.base.undraw()
        self.base = Circle(Point(self.xpos, self.ypos), self.size)
        self.base.setFill(self.color)
        self.base.setOutline("red")
        self.base.draw(self.win)

class Fighter(GameObject):

    def adjVel(self, amt):
        # if self.vel < 300: # not relevant with the air resistance working
        self.xvel = self.xvel + cos(self.angle)*amt
        self.yvel = self.yvel + sin(self.angle)*amt

    def adjAngle(self, amt):
        self.angle = self.angle + radians(amt)

    def redraw(self):
        super().redraw()
        self.arrow.undraw()
        self.vel = sqrt(self.xvel**2+self.yvel**2)
        pt1 = Point(self.xpos, self.ypos)
        pt2 = Point(self.vel*cos(self.angle) + self.xpos,
                    self.vel*sin(self.angle) + self.ypos)
        self.arrow = Line(pt1, pt2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setWidth(4)

    def fire(self, size, color):
        return Missle(self.win, self.angle, self.xpos, self.ypos, size, color)

    def update(self, time, bhlist):

        super().update(time, bhlist)
        self.yvel *= 0.99
        self.xvel *= 0.99

    def __init__(self, win, size = 7, color = "purple", angle = (pi)/2, xpos = 400, ypos = 400):

        self.mass = 180
        super().__init__(win, size, color, angle, xpos, ypos)
        self.arrow = Line(Point(400,400), Point(400,410)).draw(win)
        self.redraw()

class Missle(GameObject):
    def __init__(self, win, angle, xpos, ypos, size = 5, color = "blue"):
        super().__init__(win, size, color, angle, xpos, ypos)
        self.fuel = 0
        self.xvel = 350 * cos(angle)
        self.yvel = 350 * sin(angle)

    def update(self, time):

        super().update(time)
        self.fuel +=1

# class Obstacle(GameObject):
#      def __init__(self, win, fx, fy, mass, bx = None, by = None):
#         self.mass = mass
#         self.angle = radians(random.randint(1,360))
#         vel = 3 * random.randint(5, 15)
#         if bx: xpos, ypos = bx, by
#         else:
#             xpos = (fx + random.randint(.1 * win.trans.xmax, .9 * win.trans.xmax)) % win.trans.xmax
#             ypos = (fy + random.randint(.1 * win.trans.ybase, .9 * win.trans.ybase)) % win.trans.ybase
#         super().__init__(win, self.mass % 100, "black", self.angle, xpos, ypos)
#         self.xvel = vel * cos(self.angle)
#         self.yvel = vel * sin(self.angle)   

class BlackHole(GameObject):
    def __init__(self, win, fx, fy, mass = 0, bx = None, by = None):
        if mass == 0: self.mass = 100 * random.randint(4, 8)
        else: self.mass = mass
        self.angle = radians(random.randint(1,360))
        vel = 3 * random.randint(5, 15)
        if bx: xpos, ypos = bx, by
        else:
            xpos = (fx + random.randint(.15 * win.trans.xmax, .85 * win.trans.xmax)) % win.trans.xmax
            ypos = (fy + random.randint(.15 * win.trans.ybase, .85 * win.trans.ybase)) % win.trans.ybase
        super().__init__(win, self.mass // 10, "black", self.angle, xpos, ypos)
        self.xvel = vel * cos(self.angle)
        self.yvel = vel * sin(self.angle)

    def update(self, time, bhlist):

        super().update(time, bhlist)
        self.mass -=1
        self.size = self.mass // 10
        # self.yvel *= 0.88
        # self.xvel *= 0.88
        if abs(self.yvel) > 12: self.yvel *= 0.8
        if abs(self.xvel) > 12: self.xvel *= 0.8

class Asteroid(GameObject):
    def __init__(self, win, fx, fy, mass = 0, bx = None, by = None):
        if mass == 0: self.mass = 600
        else: self.mass = mass
        self.angle = radians(random.randint(1,360))
        vel = 10 * random.randint(30, 35) - (self.mass // 4)
        if bx: xpos, ypos = bx, by
        else:
            xpos = (fx + random.randint(.1 * win.trans.xmax, .9 * win.trans.xmax)) % win.trans.xmax
            ypos = (fy + random.randint(.1 * win.trans.ybase, .9 * win.trans.ybase)) % win.trans.ybase
        super().__init__(win, self.mass // 15, "sienna4", self.angle, xpos, ypos)
        self.xvel = vel * cos(self.angle)
        self.yvel = vel * sin(self.angle)

    def update(self, time, bhlist):

        super().update(time, bhlist)
        if abs(self.yvel) > 170: self.yvel *= 0.99
        if abs(self.xvel) > 170: self.xvel *= 0.99