
"""
licenced under the GNU Affero General Public License v3.0 (AGPL3)
This file is used for the PyPen.

This code was written mostly by me, yet I used AI to add math to Triangle, Square and VertexSquare. Also I used it for function descriptions. Rest of the logic was made by me.
Yes, it defies the "no ai" rule, BUT i didn't vibe code, i just used it to tidy up my code, and eliminate inconsistencies across all shapes. 

Yes but you mind ask, "BUT YOU DON'T KNOW GEOMETRY?!". dumbasses i am 6th grade HOW THE FUQ I AM SUPPOSED TO KNOW SHOELACE FORMULA?!
or the other complicated shi.
So please, no hate. Trying to quit vibe coding.

Changelog - V1.2:
- Support for movement and unified draw()
"""

import turtle


class PyPen:
    def __init__(self, title: str):
        self.screen = turtle.Screen()
        self.screen.title(title)
        self._turtle = turtle.Turtle()

    def initialise(self, color: str, size: int, speed: int):
        self.screen.tracer(0)  # <- add this
        self._turtle.hideturtle()
        self._turtle.pendown()
        self._turtle.color(color)
        self._turtle.pensize(size)
        self._turtle.speed(speed)

    def clear(self):
        self._turtle.clear()

    def stopDrawing(self):
        self._turtle.penup()

    def startDrawing(self):
        self._turtle.pendown()

    def initFill(self, color: str):
        self._turtle.fillcolor(color)
        self._turtle.begin_fill()

    def endFill(self):
        self._turtle.end_fill()

    def rotate(self, deg: float):
        if deg < 0:
            self._turtle.left(abs(deg))
        else:
            self._turtle.right(deg)

    def move(self, units: float):
        if units < 0:
            self._turtle.backward(abs(units))
        else:
            self._turtle.forward(units)

    def tp(self, x: float, y: float):
        self._turtle.goto(x, y)

    # ── unified draw ──────────────────────────────────────────────────────────

    def draw(self, target, color: str = "black", fill: bool = False):
        """
        Draw any shape or Movement instance.

        Parameters
        ----------
        target : shape or Movement
            Anything with a get_vertices() method.
        color  : str
            Pen (and fill) color.
        fill   : bool
            Whether to fill the shape.
        """
        if not hasattr(target, "get_vertices"):
            raise TypeError(
                f"PYPEN ERR: {type(target).__name__} has no get_vertices() method. "
                "Make sure your shape implements get_vertices()."
            )

        vertices = target._apply_transform(target.get_vertices())
        if not vertices:
            return

        self._turtle.color(color)

        # lift pen and jump to the first vertex
        self._turtle.penup()
        self._turtle.goto(vertices[0])

        if fill:
            self._turtle.fillcolor(color)
            self._turtle.begin_fill()

        self._turtle.pendown()

        for pt in vertices[1:]:
            self._turtle.goto(pt)

        # close the shape only when it has more than 2 points (i.e. not a Line)
        if len(vertices) > 2:
            self._turtle.goto(vertices[0])

        self._turtle.penup()

        if fill:
            self._turtle.end_fill()

    