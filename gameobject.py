from graphics import *
from math import sin, cos, radians, degrees, sqrt

class GameObject:
    def __init__(self, win, size, color, xpos=0, ypos=0):
        self.base = Circle(Point(xpos, ypos), size)
        self.base.setFill(color)
        self.base.setOutline("red")
        self.base.draw(win)
        self.win = win
        self.angle = radians(90.0)
        self.vel = 0.0
        self.xvel = 0.0
        self.yvel = 0.0
        self.ypos = ypos
        self.xpos = xpos


    def update(self, time):

        self.vel = sqrt(self.xvel**2+self.yvel**2)
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

    def adjAngle(self, amt):
        self.angle = self.angle + radians(amt)

class Fighter(GameObject):

    def adjVel(self, amt):
        if self.vel < 1350: #not relevant with the air resistance working
            self.xvel = self.xvel + cos(self.angle)*amt
            self.yvel = self.yvel + sin(self.angle)*amt


    def redraw(self):
        self.arrow.undraw()
        self.base.undraw()
        pt1 = Point(self.xpos, self.ypos)
        pt2 = Point(self.vel*cos(self.angle) + self.xpos,
                    self.vel*sin(self.angle) + self.ypos)
        self.arrow = Line(pt1, pt2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setWidth(4)
        self.base = Circle(pt1, 7)
        self.base.setFill("purple")
        self.base.setOutline("red")
        self.base.draw(self.win)

    def fire(self, size, color):
        return ShotTracker(self.win, degrees(self.angle),
                           400, self.xpos, self.ypos, size, color)

    def update(self, time):

        super().update(time)
        self.yvel *= 0.99
        self.xvel *= 0.99

    def __init__(self, win, size = 7, color = "purple", xpos = 400, ypos = 400):

        super().__init__(win, size, color, xpos, ypos)
        self.arrow = Line(Point(400,400), Point(400,410)).draw(win)
        self.redraw()
