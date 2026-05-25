
"""
licenced under the GNU Affero General Public License v3.0 (AGPL3)
This file is used for testing the Sketchable Library.                    
"""



from pydraw import *

pen = PyPen("square chaos")
pen.initialise("white", 2, Speed.INSTANT, "black")

# ── squares ─────────────────────────────

s1 = Square(50)
s1.move_to(-100, -50)

s2 = Square(40)
s2.move_to(80, 60)

s3 = Square(70)
s3.move_to(0, 0)

# ── motion ──────────────────────────────

m1 = Motion(s1, pen, vx=3, vy=2,collidable=[s2, s3], CanExitWindow=False)
m2 = Motion(s2, pen, vx=-2, vy=3.5,collidable=[s1, s3], CanExitWindow=False)
m3 = Motion(s3, pen, vx=1.5, vy=-2.5,collidable=[s1, s2], CanExitWindow=False)

# ── loop ────────────────────────────────

while True:
    pen.clear()

    pen.draw(s1,color="white",fill=True)
    pen.draw(s2,color="red",fill=True)
    pen.draw(s3,color="blue",fill=True)

    m1.update()
    m2.update()
    m3.update()