<p align="center"> <a href="https://postimg.cc/Pvk711WP"> <img src="https://i.postimg.cc/pr8R5CxV/Chat-GPT-Image-May-11-2026-02-50-51-PM-removebg-preview.png" alt="no more image *sob*" /> </a> </p>


<h1 align="center">Documentation for the PyDraw Graphical Library(PGL)</h1>

> [!NOTE]
> PyDraw is leaving W.I.P(Pre-Release) soon!
> I think I'll get it ready for mass-use when ill squash all bugs.
> Official release will happen on version 2.0 or 1.5.
> Ill announce the final Pre-Release soon.
> Also since there are so many projects named PyDraw, submit your idea for a new name: https://forms.gle/8p6pJ7tybQe94ENC8

> [!NOTE]
> The Licence has been changed from AGPL to MIT.

> [!TIP]
> this is my first project after stopping vibe-coding. it does have bugs, and for some features i indeed used AI to help me implement them.
> This also means there are some bugs, and if you see one:
> #### **WRITE AN ISSUE**.
> i _beg_ you. 

The software is distributed under the terms of the MIT License.
or in more simpler terms - if you fork/use it in an separate repo, give credit. easy.

# I - Capabilities and installation:
- **Primitives(basic shapes):** Squares, Circles, Triangles, and more, with their geometrical operations(area, perrimeter, etc)
- **Custom shapes(via Vertex):** Since PyDraw is based on the Vertex(basic x and y coodronates), you can make Polygons(with an unlimited nr of Vertexes), or an VertexSquare(an square made of vertexes)
- **Motion, basic physics and collisions:** The Vertex also helps with collisions, making every shape you do colide(of course, only moveable ones). You just define a shape, then you can move/rotate it or resize it!
- **Fast updates:** i am updating this library quite often! Especially bugfixes, my ahh can't make some nice code. Bugfixes will be part of most updates, so you can enjoy the smoothest, most stable experience! also we have issues so you can report bugs/suggestions there. 
- **monke hear monke do:** i listen to feedback and i implement your ideas(but please don't make them too wacky)

## II - Installation
1. Via `.url`: Open the latest release, run the .url file and run the command from the site.
2. Via `pip`: run `pip install pydraw-turtle`, and `pip install --upgrade pydraw-turtle` for updating.

# III - How2Use:

## 1. Shapes and their initialisations(one with ※ can be used with the Motion class):
- ※`Vertex`: `vertex = Vertex(x: float, y: float)`
- `Circle`: `circle = Circle(center: Vertex, radius: float)`
- ※`Triangle`: `triangle = Triangle(v1: Vertex, v2: Vertex, v3: Vertex)`
- ※`Square`: `square = Square(side: int)`
- ※`VertexSquare`: `vsquare = VertexSquare(v1: Vertex, v2: Vertex, v3: Vertex, v4: Vertex)`
- `Elipse`: `elipse = Elipse(center: Vertex, a: float, b: float)`
- ※`RegularPolygon(n-sided shape`: `rpoly = RegularPolygon(sides: int, side_lenght: float)`
- ※`Polygon:` `poly = Polygon(vertecies: list)` (make a list full of vertecies)

## 2. Functions:
(all shapes exept vertex have get_vertices())
- #### Vertex: `getvX()`; `getvY()`
- #### Line: `lenght()`; `midpoint()`, `slope()`
- #### Circle: `getX()`; `getY()`; `getRadius()`; `area()`; `circ()`; `diam()`; `contains_point()`
- #### Triangle: `side_lenghts()`; `perimeter()`; `area()`; `is_equilateral()`; `is_isosceles()`; `is_right()`
- #### Square: `area()`; `perimeter()`; `diagonal()`
- #### VertexSquare: `area()`; `perimeter()`
- #### Ellipse: `area()`; `approx_perimeter()`; `contains_point()`
- #### RegularPolygon: `perimeter()`; `interior_angle()`; `apothem()`; `area()`
- #### Polygon: `area()`

## 3. Importing:
You can import all the things PyDraw has by writing `from pydraw import *` (not avabile for versions prior to 1.3.2)
If your version is 1.3.1, then write `from pydraw import <what component you would want>`
And if your version is prior to 1.3.1, write `from core import <what component you would want to import>`

## 4. Movement:
- For 1.3.1 and above: Use the Motion class, with the functions `move_to()`; `move_by()`; `set_velocity()`; `accelerate()`; `stop()`; `check_edge_collision()`; `is_on_screen()`; `update()`.
Example code:
```python
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

m1 = Motion(s1, pen, vx=3, vy=2)
m2 = Motion(s2, pen, vx=-2, vy=3.5)
m3 = Motion(s3, pen, vx=1.5, vy=-2.5)

# ── loop ────────────────────────────────

while True:
    pen.clear()

    pen.draw(s1, color="white", fill=True)
    pen.draw(s2, color="red", fill=True)
    pen.draw(s3, color="blue", fill=True)

    m1.update()
    m2.update()
    m3.update()

    # bounce logic
    if not m1.is_on_screen():
        m1.vx *= -1
        m1.vy *= -1

    if not m2.is_on_screen():
        m2.vx *= -1
        m2.vy *= -1

    if not m3.is_on_screen():
        m3.vx *= -1
        m3.vy *= -1
```
- For version 1.2.0 use the `Moveable` class, that has the same movement commands as `Motion`, but whiout the collision stuff,
and of course, whiout updating(you need to do it manually via pen.clear() ).
Example code:
```python
import os
import sys
from core import PyPen, Square, Triangle, Vertex, Moveable
from turtle import *
import time

pen = PyPen("dvd!")

pen.initialise("black", 1, 1)

cube = Square(60).move_to(100, 100)

dx, dy = 3, 2  # velocity (speed in x and y)

while True:
    pen.clear()

    # move cube
    cube.move_by(dx, dy)

    x, y = cube.position
    size = cube.side

    # screen bounds (you may tweak these depending on your window)
    left, right = -395, 395
    bottom, top = -330, 330

    # bounce logic
    if x < left or x + size > right:
        dx *= -1

    if y < bottom or y + size > top:
        dy *= -1

    pen.draw(cube, color="purple", fill=True)

    pen.screen.update()
    time.sleep(0.01)
```

# III - Contribuiting and reporting bugs:
You can tell me what issues PyDraw has(because i don't test it too often), by going into the issues section of GitHub.
Also, you can suggest me some new ideas there too. Forking is allowed, and you can fork freely, and even merge with the main repo.
But if you make your own fork, be sure to give credit.

Made with 💔- ugh i mean 💖 and not 🤖 by Brickboss <3
