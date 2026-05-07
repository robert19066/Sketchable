
import turtle


class PyPen:
    def __init__(self, title):
        self.screen = turtle.Screen()
        self.screen.title(title) 
        
        self._turtle = turtle.Turtle()

    def initialise(self, color, size, speed):
        self._turtle.isvisible(False)
        self._turtle.pendown()
        self._turtle.color(color)
        self._turtle.pensize(size)
        self._turtle.speed(speed)
        

    def reset(self):
        self._turtle.reset()

    def stopDrawing(self):
        self._turtle.penup()

    def startDrawing(self):
        self._turtle.pendown()

    def initFill(self, color):
        self._turtle.fillcolor(color)
        self._turtle.begin_fill()

    def endFill(self):
        self._turtle.end_fill()

    def rotate(self, deg):
        if deg < 0:
            self._turtle.left(abs(deg))
        else:
            self._turtle.right(deg)

    def move(self, units):
        if units < 0:
            self._turtle.backward(abs(units))
        else:
            self._turtle.forward(units)

    def tp(self, x, y):
        self._turtle.goto(x, y);