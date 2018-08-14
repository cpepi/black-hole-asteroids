from graphics import *
from launcher import Launcher


class ProjectileApp:

    def __init__(self):

        self.win = GraphWin("Projectile Animation", 640, 480)
        self.win.setCoords(-10, -10, 210, 155)
        self.launcher = Launcher(self.win)
        self.shots = []
        self.autofire = False
        self.firerate = False
        Line(Point(-10, 0), Point(210, 0)).draw(self.win)
        for x in range(0, 210, 50):
            Text(Point(x, -7), str(x)).draw(self.win)
            Line(Point(x, 0), Point(x, 2)).draw(self.win)

    def run(self):

        while True:
            self.updateShots(1/30)
            key = self.win.checkKey()
            if key in ['q', 'Q']:
                break
            if key == "1":
                self.launcher.adjAngle(3)
            elif key == "3":
                self.launcher.adjAngle(-3)
            elif key == "5":
                self.launcher.adjVel(5)
            elif key == "2":
                self.launcher.adjVel(-5)
            elif key == "Up":
                self.launcher.adjHeight(3)
            elif key == "Down":
                self.launcher.adjHeight(-3)
            elif key == "Right":
                self.launcher.adjX(3)
            elif key == "Left":
                self.launcher.adjX(-3)
            elif key == "6":
                self.autofire = not self.autofire
            if self.autofire == True:
                if self.firerate == True:
                    self.shots.append(self.launcher.fire())
                    self.firerate = False
                else:
                    self.firerate = True
            else:
                if key in ["Return"]:
                    self.shots.append(self.launcher.fire())

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

# app = ProjectileApp()
# app.run()