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

    def redraw(self):
        self.arrow.undraw()
        pt2 = Point(self.vel*cos(self.angle), self.vel*sin(self.angle)+ self.height)
        self.arrow = Line(Point(0, self.height), pt2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setWidth(3)

    def fire(self):
        return ShotTracker(self.win, degrees(self.angle), self.vel, self.height)

    def __init__(self, win):
        base = Circle(Point(0, 0), 3)
        base.setFill("green")
        base.setOutline("red")
        base.draw(win)

        self.win = win
        self.angle = radians(45.0)
        self.vel = 40.0
        self.height = 0
        self.arrow = Line(Point(0, 0), Point(0, 0)).draw(win)
        self.redraw()
