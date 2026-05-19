<p align="center"> <a href="https://postimg.cc/Pvk711WP"> <img src="https://i.postimg.cc/sx9rq3vc/9e5d0f42-f7f4-4ff1-acb8-3b96980b8d1c-removalai-preview.png" alt="no more image *sob*" /> </a> </p>


<h1 align="center">Documentation for the PyDraw Game Engine(PGE)</h1>

![license](https://img.shields.io/badge/license-MIT-green?style=flat)
![Get It On](https://img.shields.io/badge/Get%20It%20On-PyPi-informational?style=flat&logo=pypi)
![Made with](https://img.shields.io/badge/Made%20with-Python-informational?style=flat&logo=python)
![Status](https://img.shields.io/badge/Status-Maintained-important?style=flat)
![Difficulty](https://img.shields.io/badge/Difficulty-Low-success?style=flat)
![Type](https://img.shields.io/badge/Type-Game%20Engine%2FLibrary-informational?style=flat)
![Made with](https://img.shields.io/badge/Made%20with-Love-red?style=flat&logo=heart)



> [!NOTE]
> PyDraw is now an GAME ENGINE!
> Also it's leaving W.I.P(Pre-Release) in version 1.5, so expect a lot of new features and optimizations, and of course, a more stable experience!
> Also since there are so many projects named PyDraw, submit your idea for a new name: https://forms.gle/8p6pJ7tybQe94ENC8
> THANK YALL FOR 200 VIEWS I LUV YOUUUUU 

> [!WARNING]
> The GitHub versions are used ONLY for showing what has changed, its NOT recomanded
> to install PyDraw from them, use `pip` instead. v1.0.0 is `pip` exclusive.
> Please don't. I am using the releases just to note the changelogs. 


# I - Capabilities and installation:
- **Primitives(basic shapes):** Squares, Circles, Triangles, and more, with their geometrical operations(area, perrimeter, etc)
- **Custom shapes(via Vertex):** Since PyDraw is based on the Vertex(basic x and y coodronates), you can make Polygons(with an unlimited nr of Vertexes), or an VertexSquare(an square made of vertexes)
- **Motion, basic physics and collisions:** The Vertex also helps with collisions, making every shape you do colide(of course, only moveable ones). You just define a shape, then you can move/rotate it or resize it!
- **Keyboard Input:** The library supports listening for keyboard input, allowing you to create interactive applications.
- **Sound:** The library also has a sound module that can play WAV files natively, and can decode and play other formats with FFmpeg installed.
- **Fast updates:** i am updating this library quite often! Especially bugfixes, my ahh can't make some nice code. Bugfixes will be part of most updates, so you can enjoy the smoothest, most stable experience! also we have issues so you can report bugs/suggestions there. 

## II - Installation
1. Via `.url`: Open the latest release, run the .url file and run the command from the site.
2. Via `pip`: run `pip install pydraw-turtle`, and `pip install --upgrade pydraw-turtle` for updating.
> [!IMPORTANT]
> Due to me having a severe skill issue, the dependencies might not install.
> idk why. So, for now on, every release will have the `requirements.txt` with the list of
> dependencies. Just install them, and PyDraw will work perfectly fine and dandy.

# III - How2Use:

## 1. Shapes and their initialisations(one with ※ can be used with the Motion class):

In PyDraw, all shapes rely on the crucial `Vertex`. It is an uni-dimensional imaginary dot with an set of coordonates, from where all primitives are based!
And in version 1.3.5, the `Cluster` has been added(and the list specifies what shapes are Cluster-compatible) that is an array of `Vertex` elements.
The methods `Cluster` has are:

- `from_list(list[Vertex])` - Converts an List full of vertexes into an `Cluster`
- `add(v: Vertex)` - Adds an `Vertex`
- `remove(index: int)` - Removes an `Vertex` from an index.
- `pop(index: int)` - Removes and returns an `Vertex` from an index.
- `shift_to(index: int, vx: float, vy: float)` and `shift_by(same arguments` - Moves to/by an `Vertex` from an index)


List of shapes and their initialisations:
- ※`Line`: `line = Line(v1: Vertex, v2: Vertex/vertexes: Cluster)`
- ※`Vertex`: `vertex = Vertex(x: float, y: float)`
- `Circle`: `circle = Circle(center: Vertex, radius: float)`
- ※`Triangle`: `triangle = Triangle(v1: Vertex, v2: Vertex, v3: Vertex/vertexes: Cluster)`
- ※`Square`: `square = Square(side: int)`
- ※(formerly VertexSquare)`CustomSquare`: `vsquare = CustomSquare(v1: Vertex, v2: Vertex, v3: Vertex, v4: Vertex/vertexes: Cluster)`
- ~`Elipse`: `elipse = Elipse(center: Vertex, a: float, b: float)`~ (has been depricated and removed prior to v1.3.5, because its lowk useless.)
- ※(formerly RegularPolygon)`SidePolygon(n-sided shape)`: `rpoly = SidePolygon(sides: int, side_lenght: float)`
- ※(formerly Polygon)`Mesh:` `poly = Mesh(vertecies: list/vertecies: Cluster)` (make a list full of vertecies)


## 3. Importing:
You can import all the things PyDraw has by writing `from pydraw import *` (not avabile for versions prior to 1.3.2)
If your version is 1.3.1, then write `from pydraw import <what component you would want>`
And if your version is prior to 1.3.1, write `from core import <what component you would want to import>`

## 4. Movement:

PyDraw also suports movement, using the `Motion` class. To initialise the `Motion` class with an shape that is `Movable`, do:
`mov = Motion(shape, pen, vx, vy, colidable, CanExitWindow)`

What they mean:
- `shape` - Any shape that is `Moveable`.
- `pen: PyPen` - An `PyPen` instance.
- `vx: float` and `vy: float` - The initial coordonates.
- `colidable: List` - An list of shapes that the current shape CAN colide(if you don't set it, it will default to None).
- `CanExitWindow: Bool` - If the shape colides with the window corner.

- For 1.3.1 and above: Use the Motion class, with the functions: 
- `move_to(vx: float, vy: float)`; 
- `move_by(vx: float, vy: float)`; 
- `set_velocity(vx: float, vy: float)`; 
- `accelerate(ax: float, ay: float)`; 
- `stop()`; 
- `check_edge_collision()`; 
- `is_on_screen()`; 
- `update()`.
- 
##### Example code:
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

m1 = Motion(s1, pen, vx=3, vy=2, CanExitWindow=False)
m2 = Motion(s2, pen, vx=-2, vy=3.5, CanExitWindow=False)
m3 = Motion(s3, pen, vx=1.5, vy=-2.5, CanExitWindow=False)

# ── loop ────────────────────────────────

while True:
    pen.clear()

    pen.draw(s1,color="white",fill=True)
    pen.draw(s2,color="red",fill=True)
    pen.draw(s3,color="blue",fill=True)

    m1.update()
    m2.update()
    m3.update()
```
- For version 1.2.0 use the `Moveable` class, that has the same movement commands as `Motion`, but whiout the collision stuff,
and of course, whiout updating(you need to do it manually via pen.clear() ).
##### Example code:
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

> [!TIP]
> If you need to transition from `Moveable` to `Motion`, you just need to add `mov = Motion(shape, pen, vx and vy)`, and it will automaticly
> change from `Moveable` to `Motion`. And yes if you want `Moveable` instead of `Motion` just don't initialise it.
> its called backwards compatability :D
> (i think)

# IV - Sound:
PyDraw has a sound module, that can play WAV files natively, and can decode and play other formats with FFmpeg installed. You can use the `Speakers` class to play audio
files. Just create an instance of `Speakers` with the path to your audio file, and call the `play()` method to play it. If your file is not a WAV file, you can call the `decode()` method first with the appropriate file type (e.g., "mp3", "ogg", etc.) to decode it into memory before playing.
##### Example code:
```python
from pydraw import Speakers
speaker = Speakers("path/to/your/audiofile.mp3")
speaker.decode("mp3")
speaker.play()
```

# V - Keyboard input:
PyDraw also has a keyboard module that allows you to listen to keyboard input. You can use the `Keyboard` class to listen for key presses. Just create an instance of `Keyboard`, and call the `start_listening()` method to start listening for keyboard input. You can also specify a callback function that will be called whenever a key is pressed.
##### Example code:
```python
from pydraw import Keyboard
kb = Keyboard()
kb.start_listening()

while True:
    if kb.is_pressed(pynput.keyboard.Key.space):
        print(True)
    else:
        print(False)
```
# VI - Contribuiting and reporting bugs:
You can tell me what issues PyDraw has(because i don't test it too often), by going into the issues section of GitHub.
Also, you can suggest me some new ideas there too. Forking is allowed, and you can fork freely, and even merge with the main repo.
But if you make your own fork, be sure to give credit.

For this project i used the folowing OSS python libaries:
- Pyinstaller
- Pynput
- Simpleaudio
(so don't DMCA me)

Made with 💔- ugh i mean 💖 by Brickboss <3
Licensed over the Pydraw-MIT(PMIT) licence - This license is based on the MIT License and is intended to be compatible with it
