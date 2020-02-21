"""
This is the player for a basic asteroids game. It only works on windows
now and requires Python 3+.
"""
import graphics
from graphics import *
from gameobject import *
import time

class BHApp:

    def __init__(self, high):

        self.win = GraphWin("BH Animation", 1180, 760)
        self.win.setCoords(-0, 0, 1180, 760)
        self.shots = []
        self.bh = []
        self.ast = []
        self.score = 0
        self.score_text = Text(Point(50, self.win.trans.ybase - 30), self.score).draw(self.win)
        self.high_score = high
        self.firerate = 0
        self.fighter = Fighter(self.win)
        self.pressed = {}
        self.set_bindings()

    def set_bindings(self):
        for char in ["Return","q","Q","Left","Right","Up","Down","b"]:
            graphics._root.bind("<KeyPress-{0}>".format(char), self._pressed)
            graphics._root.bind("<KeyRelease-{0}>".format(char), self._released)
            self.pressed[char] = False

    def death(self):
        d_list = ["YOU DIED", "THANKS OBAMA", "HELLO THERE"]
        text = Text(Point(600, 400), d_list[self.score //100 % 3])
        text.setSize(36)
        text.setTextColor("firebrick2")
        text.setStyle("bold")
        return text

    def animate(self):
        if self.pressed["Return"]:
            if self.firerate % 4 == 0: self.shots.append(self.fighter.fire(5, "blue"))
            self.firerate +=1
        if self.pressed["Up"]: self.fighter.adjVel(5); self.fighter.color = "yellow"
        if self.pressed["Down"]: self.fighter.adjVel(-3)
        if self.pressed["Left"]: self.fighter.adjAngle(4)
        if self.pressed["Right"]: self.fighter.adjAngle(-4)
        if self.pressed["b"]: self.bh.append(BlackHole(self.win, self.fighter.xpos,self.fighter.ypos))


    def _pressed(self, event):
        self.pressed[event.keysym] = True

    def _released(self, event):
        self.pressed[event.keysym] = False
        if event.keysym == "Return": self.firerate = 0
        if event.keysym == "Up": self.fighter.color = "purple"

    def run(self):

        Text(Point(30, self.win.trans.ybase - 10), "SCORE").draw(self.win)
        Text(Point(150, self.win.trans.ybase - 10), "HIGH SCORE").draw(self.win)
        Text(Point(150, self.win.trans.ybase - 30), self.high_score).draw(self.win)

        while True:

            if self.pressed["q"] or self.pressed["Q"]: break
            self.updateShots(1/30)
            self.updateBH(1/30)
            self.updateAST(1/30)
            self.fighter.update(1/30, self.bh)
            self.animate()
            update(30)

        self.win.close()

    def updateShots(self, dt):
        alive = []
        for shot in self.shots:
            shot.update(dt)
            if shot.fuel < 120:
                alive.append(shot)
            else:
                shot.base.undraw()
        self.shots = alive

    def updateBH(self, dt):
        alive = []
        for bh in self.bh:
            bh.update(dt, self.bh)
            if collision(self.fighter, bh):
                high_score = self.score if self.score > self.high_score else self.high_score
                self.death().draw(self.win)
                time.sleep(2)
                self.win.close()
                BHApp(high_score).run() 
            if bh.mass > 20:
                alive.append(bh)
            else:
                bh.base.undraw()
        if len(alive) > 1:
            for hole in alive:
                temp = alive[:]
                temp.remove(hole)
                for hole2 in temp:
                    if collision(hole, hole2):
                        alive.append(BlackHole(self.win, self.fighter.xpos,self.fighter.ypos,
                        (.75 * (hole.mass + hole2.mass)), (hole.xpos+hole2.xpos)/2,(hole.ypos+hole2.ypos)/2))
                        hole.base.undraw()
                        hole2.base.undraw()
                        alive.remove(hole)
                        alive.remove(hole2)
                        break
        if len(alive) < self.score // 6000 + 1:
            alive.append(BlackHole(self.win, self.fighter.xpos,self.fighter.ypos))
        self.bh = alive

    def updateAST(self, dt):
        alive = []
        for ast in self.ast:
            ast.update(dt, self.bh)
            if collision(self.fighter, ast):
                high_score = self.score if self.score > self.high_score else self.high_score
                self.death().draw(self.win)
                time.sleep(2)
                self.win.close()
                BHApp(high_score).run() 

            status = True
            for shot in self.shots:
                if collision(ast, shot):
                    ast.base.undraw()
                    shot.base.undraw()
                    self.shots.remove(shot)
                    status = False
                    self.score += ast.mass
                    self.score_text.undraw()
                    self.score_text = Text(Point(50, self.win.trans.ybase - 30), self.score).draw(self.win)
                    if self.score % 2000 == 0: alive.append(Asteroid(self.win, self.fighter.xpos,self.fighter.ypos))
                    break

            if status:
                if self.bh:
                    for bh in self.bh:
                        if collision(ast, bh):
                            ast.base.undraw()
                            status = False
                            bh.mass += ast.mass // 40
                            # self.score -= ast.mass // 50
                            # self.score_text.undraw()
                            # self.score_text = Text(Point(50, self.win.trans.ybase - 30), self.score).draw(self.win)

            if status: alive.append(ast)
            else: 
                for _ in range(((ast.mass + 100) % 300) // 40):
                    alive.append(Asteroid(self.win, self.fighter.xpos,self.fighter.ypos,
                    ast.mass - 200, ast.xpos, ast.ypos))
        if self.firerate % 30 == 0 and not self.firerate == 0:
            alive.append(Asteroid(self.win, self.fighter.xpos,self.fighter.ypos)) 
        if len(alive) < self.score // 5000 + 2:
            alive.append(Asteroid(self.win, self.fighter.xpos,self.fighter.ypos))
        self.ast = alive

if __name__ == "__main__":
    BHApp(0).run()