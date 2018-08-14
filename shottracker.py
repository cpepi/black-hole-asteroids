from proj import Projectile
import graphics as g

class ShotTracker:

    def __init__(self, win, angle, velocity, xval, height):

        self.proj = Projectile(angle, velocity, xval, height)
        self.marker = g.Circle(g.Point(xval, height), 3)
        self.marker.setFill("blue")
        self.marker.setOutline("red")
        self.marker.draw(win)

    def update(self, dt):

        self.proj.update(dt)
        center = self.marker.getCenter()
        dx = self.proj.getX() - center.getX()
        dy = self.proj.getY() - center.getY()
        self.marker.move(dx, dy)

    def getX(self):
        return self.proj.getX()

    def getY(self):
        return self.proj.getY()

    def undraw(self):
        self.marker.undraw()
