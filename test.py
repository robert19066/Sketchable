
"""
licenced under the GNU Affero General Public License v3.0 (AGPL3)
This file is used for testing the PyDraw Library.                    
"""

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