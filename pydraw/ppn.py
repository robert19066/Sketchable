
"""
licenced under the MIT licence
This file is used for the PyPen.

This code was written by me.(100%)

Changelog(only changes if the file was changed :) )  - V1.3:
- more functions
"""

from time import sleep
import turtle

from enum import Enum

class Speed(Enum):
    """
    Speed|Turtle equivalent
    SLUGGISH:1
    SLOWER:2
    QUITE_SLOW:3
    SLOW:4
    MEDIUM:5
    QUITE_FAST:6
    FASTER:7
    VERRY_FAST:8
    SUPER_FAST:9
    ALMOST_INSTANT:10
    INSTANT:0
    """
    SLUGGISH = 1
    SLOWER = 2
    QUITE_SLOW = 3
    SLOW = 4
    MEDIUM = 5
    QUITE_FAST = 6
    FASTER = 7
    VERY_FAST = 8
    SUPER_FAST = 9
    ALMOST_INSTANT = 10
    INSTANT = 0


class PyPen:
    def __init__(self, title: str):
        self.screen = turtle.Screen()
        self.screen.title(title)
        self._turtle = turtle.Turtle()

    def initialise(self, PenColor: str, size: int, speed: str, BackgroundColor: Speed):
        """
        INITIALISES AN PYPEN!
        Arguments:
        - PenColor - pen color
        - Size - pen size
        - Speed - Pen speed("sluggish", "slower", "quite slow", "slow", "medium", "quite fast", "faster", "verry fast", "really fast", "super fast", "almost instant", "instant")
        - BackgroundColor - the color of the ground.
        """
        self.screen.tracer(0)  # <- for smooth movement =)
        self._turtle.hideturtle()
        self._turtle.pendown()
        self._turtle.screen.bgcolor(BackgroundColor)
        self._turtle.color(PenColor)
        self._turtle.pensize(size)
        if (speed == Speed.SLUGGISH):
            self._turtle.speed(1)
        elif (speed == Speed.SLOWER):
            self._turtle.speed(2)
        elif (speed == Speed.QUITE_FAST):
            self._turtle.speed(3)
        elif (speed == Speed.SLOW):
            self._turtle.speed(4)
        elif (speed == Speed.MEDIUM):
            self._turtle.speed(5)
        elif (speed == Speed.QUITE_FAST):
            self._turtle.speed(6)
        elif (speed == Speed.FASTER):
            self._turtle.speed(7)
        elif (speed == Speed.VERY_FAST):
            self._turtle.speed(8)
        elif (speed == Speed.SUPER_FAST):
            self._turtle.speed(9)
        elif (speed == Speed.ALMOST_INSTANT):
            self._turtle.speed(10)
        elif (speed == Speed.INSTANT):
            self._turtle.speed(0)

    def clear(self):
        """
        """
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

    