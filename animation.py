from proj import Projectile
from button import Button
import graphics as g

class ShotTracker:
    
    def __init__(self, win, angle, velocity, height):

        self.proj = Projectile(angle, velocity, height)
        self.marker = g.Circle(g.Point(0, height), 3)
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

class InputDialog:

    def __init__(self, angle, vel, height):

        self.win = win = g.GraphWin("Initial Values", 200, 300)
        win.setCoords(0, 4.5, 4, 0.5)

        g.Text(g.Point(1, 1), "Angle").draw(win)
        self.angle = g.Entry(g.Point(3, 1), 5).draw(win)
        self.angle.setText(str(angle))

        g.Text(g.Point(1, 2), "Velocity").draw(win)
        self.vel = g.Entry(g.Point(3, 2), 5).draw(win)
        self.vel.setText(str(vel))

        g.Text(g.Point(1, 3), "Height").draw(win)
        self.height = g.Entry(g.Point(3, 3), 5).draw(win)
        self.height.setText(str(height))

        self.fire = Button(win, g.Point(1, 4), 1.25, 0.5, "Fire")
        self.fire.activate()

        self.quit = Button(win, g.Point(3, 4), 1.25, 0.5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt= self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        h = float(self.height.getText())
        return a, v, h

    def close(self):
        self.win.close()
        
def main():

    win = g.GraphWin("Cannonball Animation", 640, 480, autoflush = False)
    win.setCoords(-10, -10, 210, 155)

    g.Line(g.Point(-10, 0), g.Point(210, 0)).draw(win)

    for x in range(0, 210, 50):
        g.Text(g.Point(x, -5), str(x)).draw(win)
        g.Line(g.Point(x, 0), g.Point(x, 2)).draw(win)

    angle, vel, height = 45.0, 40.0, 2.0

    while True:
        inputwin = InputDialog(angle, vel, height)
        choice = inputwin.interact()
        inputwin.close()

        if choice == "Quit":
            break

        angle, vel, height = inputwin.getValues()
        shot = ShotTracker(win, angle, vel, height)
        while 0 <= shot.getY() and -10 < shot.getX() <= 210:
            shot.update(1/50)
            g.update(50)

    win.close()

main()
