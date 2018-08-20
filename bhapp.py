import graphics
from graphics import *
from gameobject import *


class BHApp:

    def __init__(self):

        self.win = GraphWin("BH Animation", 1180, 760)
        self.win.setCoords(-0, 0, 1180, 760)
        self.shots = []
        self.bh = []
        self.firerate = 0
        self.fighter = Fighter(self.win)
        self.pressed = {}
        self.set_bindings()

    def set_bindings(self):
        for char in ["Return","q","Left","Right","Up","Down","b"]:
            graphics._root.bind("<KeyPress-{0}>".format(char), self._pressed)
            graphics._root.bind("<KeyRelease-{0}>".format(char), self._released)
            self.pressed[char] = False

    def animate(self):
        if self.pressed["Return"]:
            if self.firerate % 4 == 0: self.shots.append(self.fighter.fire(5, "blue"))
            self.firerate +=1
        if self.pressed["Up"]: self.fighter.adjVel(6)
        if self.pressed["Down"]: self.fighter.adjVel(-3)
        if self.pressed["Left"]: self.fighter.adjAngle(4)
        if self.pressed["Right"]: self.fighter.adjAngle(-4)
        if self.pressed["b"]: self.bh.append(BlackHole(self.win, self.fighter.xpos,self.fighter.ypos))


    def _pressed(self, event):
        self.pressed[event.keysym] = True

    def _released(self, event):
        self.pressed[event.keysym] = False
        if event.keysym == "Return": self.firerate = 0

    def run(self):

        while True:

            if self.pressed["q"]: break
            self.updateShots(1/30)
            self.updateBH(1/30)
            self.fighter.update(1/30, self.bh)
            self.animate()
            update(30)

        self.win.close()

    def updateShots(self, dt):
        alive = []
        for shot in self.shots:
            shot.update(dt)
            if shot.fuel < 150:
                alive.append(shot)
            else:
                shot.base.undraw()
        self.shots = alive

    def updateBH(self, dt):
        alive = []
        for bh in self.bh:
            bh.update(dt, self.bh)
            if bh.mass > 100:
                alive.append(bh)
            else:
                bh.base.undraw()
        if len(alive) > 1:
            for hole in alive:
                temp = alive[:]
                temp.remove(hole)
                for hole2 in temp:
                    if distance(hole, hole2) < hole.size + hole2.size:
                        alive.append(BlackHole(self.win, self.fighter.xpos,self.fighter.ypos,
                        (.75 * (hole.mass + hole2.mass)), (hole.xpos+hole2.xpos)/2,(hole.ypos+hole2.ypos)/2))
                        hole.base.undraw()
                        hole2.base.undraw()
                        alive.remove(hole)
                        alive.remove(hole2)
                        break
        if len(alive) < 3:
            alive.append(BlackHole(self.win, self.fighter.xpos,self.fighter.ypos))
        self.bh = alive

if __name__ == "__main__":
    BHApp().run()
