from proj import Projectile


def getInputs():
    a = float(input("Enter Launch Angle in deg: "))
    v = float(input("Enter Launch Velocity in m/sec: "))
    h = float(input("Enter Launch Height in m: "))
    t = float(input("Enter Time Interval in sec: "))
    return a, v, h, t

angle, vel, h0, time = getInputs()
cball = Projectile(angle, vel, h0)
print(cball.getX(), cball.getY())
while cball.getY() > 0:
    cball.update(time)
    print(cball.getX(), cball.getY())
