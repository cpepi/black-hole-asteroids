import graphics
from graphics import *
from gameobject import Fighter


class BHApp:

    def __init__(self):

        self.win = GraphWin("BH Animation", 1180, 760)
        self.win.setCoords(-0, 0, 1180, 760)
        self.shots = []
        self.firerate = 0
        self.fighter = Fighter(self.win)
        self.pressed = {}
        self.set_bindings()

    def set_bindings(self):
        for char in ["Return","q","Left","Right","Up","Down"]:
            graphics._root.bind("<KeyPress-{0}>".format(char), self._pressed)
            graphics._root.bind("<KeyRelease-{0}>".format(char), self._released)
            self.pressed[char] = False

    def animate(self):
        if self.pressed["Return"]:
            if self.firerate % 4 == 0: self.shots.append(self.fighter.fire(5, "blue"))
            self.firerate +=1
        if self.pressed["Up"]: self.fighter.adjVel(4)
        if self.pressed["Down"]: self.fighter.adjVel(-2)
        if self.pressed["Left"]: self.fighter.adjAngle(4)
        if self.pressed["Right"]: self.fighter.adjAngle(-4)


    def _pressed(self, event):
        self.pressed[event.keysym] = True

    def _released(self, event):
        self.pressed[event.keysym] = False
        if event.keysym == "Return": self.firerate = 0

    def run(self):

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
            if 0 < shot.getY() < 700 and 0 < shot.getX() < 1100:
                alive.append(shot)
            # else:
            #     shot.undraw()
        self.shots = alive

if __name__ == "__main__":
    BHApp().run()
