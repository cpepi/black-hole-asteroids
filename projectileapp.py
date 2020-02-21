"""
This is the player for a basic asteroids game. It only works on windows
now and requires Python 3+.
"""
import graphics
from graphics import *
from launcher import Launcher
from fighter import Fighter


class ProjectileApp:

    def __init__(self):

        self.win = GraphWin("Projectile Animation", 640, 480)
        # self.win = GraphWin("Projectile Animation", 1180, 760)
        self.win.setCoords(-10, -10, 210, 155)
        self.launcher = Launcher(self.win)
        self.shots = []
        self.firerate = 0
        self.fighter = Fighter(self.win, Point(100, 100))

        self.pressed = {}
        self.set_bindings()
        Line(Point(-10, 0), Point(210, 0)).draw(self.win)
        for x in range(0, 210, 50):
            Text(Point(x, -7), str(x)).draw(self.win)
            Line(Point(x, 0), Point(x, 2)).draw(self.win)

    def set_bindings(self):
        for char in ["u","i","o","p","Return","q","1","2","3","5","Left","Right","Up","Down"]:
            graphics._root.bind("<KeyPress-{0}>".format(char), self._pressed)
            graphics._root.bind("<KeyRelease-{0}>".format(char), self._released)
            self.pressed[char] = False

    def animate(self):
        if self.pressed["3"]:
            if self.launcher.xval < self.win.trans.xmax - 5: self.launcher.adjX(3)
        if self.pressed["1"]:
            if self.launcher.xval > self.win.trans.xbase + 4: self.launcher.adjX(-3)
        if self.pressed["5"]:
            if self.launcher.height < self.win.trans.ybase - 5: self.launcher.adjHeight(3)
        if self.pressed["2"]:
            if self.launcher.height > self.win.trans.ymin + 4: self.launcher.adjHeight(-3)
        if self.pressed["o"]: self.launcher.adjAngle(4)
        if self.pressed["p"]: self.launcher.adjAngle(-4)
        if self.pressed["i"]:
            if self.launcher.vel < 100: self.launcher.adjVel(5)
        if self.pressed["u"]:
            if self.launcher.vel > -100: self.launcher.adjVel(-5)
        if self.pressed["Return"]:
            if self.firerate % 4 == 0: self.shots.append(self.launcher.fire(2, "blue"))
            self.firerate +=1
        if self.pressed["Up"]: self.fighter.adjVel(2)
        if self.pressed["Down"]: self.fighter.adjVel(-2)
        if self.pressed["Left"]: self.fighter.adjAngle(4)
        if self.pressed["Right"]: self.fighter.adjAngle(-4)


    def _pressed(self, event):
        self.pressed[event.keysym] = True
        print("hey")
        print(self.pressed)

    def _released(self, event):
        self.pressed[event.keysym] = False
        if event.keysym == "Return": self.firerate = 0

    def run(self):
        # self.animate()
        # self.win.mainloop()
        while True:

            if self.pressed["q"]: break
            self.updateShots(1/30)
            self.fighter.update(1/30)
            self.animate()
            update(30)

        self.win.close()

    def updateShots(self, dt):
        alive = []
        for shot in self.shots:
            shot.update(dt)
            if shot.getY() >= 0 and -10 < shot.getX() < 210:
                alive.append(shot)
            # else:
            #     shot.undraw()
        self.shots = alive

if __name__ == "__main__":
    ProjectileApp().run()
