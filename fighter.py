from graphics import *
from math import sin, cos, radians, degrees, sqrt
from shottracker import ShotTracker

class Fighter:

    def adjAngle(self, amt):
        self.angle = self.angle + radians(amt)
        self.redraw()

    def adjVel(self, amt):
        # if selfself.vel = self.vel + amt
        # self.redraw()
        self.vel = sqrt(self.xvel**2+self.yvel**2)
        if self.vel < 80:
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
        self.arrow.setWidth(3)
        self.base = Circle(pt1, 3)
        self.base.setFill("purple")
        self.base.setOutline("red")
        self.base.draw(self.win)

    def fire(self):
        return ShotTracker(self.win, degrees(self.angle),
                           self.vel, self.xpos, self.ypos)

    def update(self, time, transf):

        self.xpos = self.xpos + time * self.xvel
        yvel_temp = self.yvel - 9.8 * time
        self.ypos = self.ypos + time * (self.yvel + yvel_temp) / 2.0
        self.yvel = yvel_temp
        if self.ypos < 0 : self.yvel *= -0.9

        self.redraw()

    def __init__(self, win, origin):
        self.base = Circle(origin, 3)
        self.base.setFill("green")
        self.base.setOutline("red")
        self.base.draw(win)

        self.win = win
        self.angle = radians(90.0)
        self.vel = 0.0
        self.xvel = 0.0
        self.yvel = 0.0
        self.ypos = 100
        self.xpos = 100
        self.arrow = Line(origin, origin).draw(win)
        self.redraw()
