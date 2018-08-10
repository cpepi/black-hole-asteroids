from math import sin, cos, radians

class Projectile:

    def __init__(self, angle, velocity, xval, height):
        self.xpos = xval
        self.ypos = height
        theta = radians(angle)
        self.xvel = velocity * cos(theta)
        self.yvel = velocity * sin(theta)

    def update(self, time):
        self.xpos = self.xpos + time * self.xvel
        yvel_temp = self.yvel - 9.8 * time
        self.ypos = self.ypos + time * (self.yvel + yvel_temp) / 2.0
        self.yvel = yvel_temp

    def getY(self):
        return self.ypos

    def getX(self):
        return self.xpos
