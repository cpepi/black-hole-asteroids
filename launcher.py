from graphics import *
from math import sin, cos, radians, degrees
from shottracker import ShotTracker

class Launcher:

    def adjAngle(self, amt):
        self.angle = self.angle + radians(amt)
        self.redraw()

    def adjVel(self, amt):
        self.vel = self.vel + amt
        self.redraw()

    def adjHeight(self, amt):
        self.height = self.height + amt
        self.redraw()

    def adjX(self, amt):
        self.xval = self.xval + amt
        self.redraw()

    def redraw(self):
        self.arrow.undraw()
        self.base.undraw()
        pt1 = Point(self.xval, self.height)
        pt2 = Point(self.vel*cos(self.angle) + self.xval,
                    self.vel*sin(self.angle) + self.height)
        self.arrow = Line(pt1, pt2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setWidth(3)
        self.base = Circle(pt1, 3)
        self.base.setFill("green")
        self.base.setOutline("red")
        self.base.draw(self.win)

    def fire(self, size, color):
        return ShotTracker(self.win, degrees(self.angle),
                           self.vel, self.xval, self.height, size, color)

    def __init__(self, win):
        self.base = Circle(Point(0, 0), 3)
        self.base.setFill("green")
        self.base.setOutline("red")
        self.base.draw(win)

        self.win = win
        self.angle = radians(45.0)
        self.vel = 40.0
        self.height = 0
        self.xval = 0
        self.arrow = Line(Point(0, 0), Point(0, 0)).draw(win)
        self.redraw()
