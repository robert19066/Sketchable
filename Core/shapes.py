
"""
licenced under the GNU Affero General Public License v3.0 (AGPL3)
This file is used for all the datatypes.

$$$$$$$\            $$$$$$$\                                   
$$  __$$\           $$  __$$\                                  
$$ |  $$ |$$\   $$\ $$ |  $$ | $$$$$$\  $$$$$$\  $$\  $$\  $$\ 
$$$$$$$  |$$ |  $$ |$$ |  $$ |$$  __$$\ \____$$\ $$ | $$ | $$ |
$$  ____/ $$ |  $$ |$$ |  $$ |$$ |  \__|$$$$$$$ |$$ | $$ | $$ |
$$ |      $$ |  $$ |$$ |  $$ |$$ |     $$  __$$ |$$ | $$ | $$ |
$$ |      \$$$$$$$ |$$$$$$$  |$$ |     \$$$$$$$ |\$$$$$\$$$$  |
\__|       \____$$ |\_______/ \__|      \_______| \_____\____/ 
          $$\   $$ |                                           
          \$$$$$$  |                                           
           \______/

This code was written mostly by me, yet I used AI to add math to Triangle, Square and VertexSquare. Also I used it for function descriptions. Rest of the logic was made by me.
Yes, it defies the "no ai" rule, BUT i didn't vibe code, i just used it to tidy up my code, and eliminate inconsistencies across all shapes. 
"""

from math import pi, sqrt, tan
from pypen import PyPen


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vertex(x={self.x}, y={self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def getvX(self):
        return self.x

    def getvY(self):
        return self.y



def _side(a: Vertex, b: Vertex) -> float:
    """Euclidean distance between two vertices."""
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

def _check_pen(pen):
    """Raise if *pen* is not a valid PyPen instance."""
    if not isinstance(pen, PyPen):
        raise TypeError("PYPEN ERR: You must pass a PyPen instance.")



class Circle:
    def __init__(self, center: Vertex, radius: float):
        if not isinstance(center, Vertex):
            raise TypeError("PYPEN ERR: center must be a Vertex.")
        self.center = center
        self.radius = radius

    def __repr__(self):
        return (f"Circle(x={self.center.getvX()}, y={self.center.getvY()}, "
                f"radius={self.radius})")

    def __eq__(self, other):
        return (self.center == other.center and self.radius == other.radius)

    # ── getters ──
    def getX(self):
        """Returns the x coordinate of the circle's center."""
        return self.center.getvX()

    def getY(self):
        """Returns the y coordinate of the circle's center."""
        return self.center.getvY()          # BUG FIX: was self.y

    def getRadius(self):
        """Returns the radius."""
        return self.radius

    # ── math ──
    def area(self):
        """Returns the circle's area."""
        return pi * self.radius ** 2

    def circ(self):
        """Returns the circle's circumference."""
        return 2 * pi * self.radius

    def diam(self):
        """Returns the circle's diameter."""
        return self.radius * 2

    def contains_point(self, vertex: Vertex) -> bool:
        """Returns True if *vertex* lies inside (or on) the circle."""
        dx = vertex.getvX() - self.center.getvX()
        dy = vertex.getvY() - self.center.getvY()
        return dx * dx + dy * dy <= self.radius ** 2

    # ── draw ──
    def draw(self, pen, color="black", fill=False):
        """Draw the circle.  Pass the PyPen instance."""
        _check_pen(pen)
        pen.stopDrawing()
        pen._turtle.goto(self.center.getvX(),
                         self.center.getvY() - self.radius)
        pen.startDrawing()
        if fill:
            pen.initFill(color)
        pen._turtle.circle(self.radius)
        if fill:
            pen.endFill()




class Triangle:
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def __repr__(self):
        return f"Triangle({self.v1}, {self.v2}, {self.v3})"

    def __eq__(self, other):
        return (self.v1 == other.v1 and
                self.v2 == other.v2 and
                self.v3 == other.v3)

    # ── math ──
    def side_lengths(self) -> tuple:
        """Returns the three side lengths (a, b, c)."""
        a = _side(self.v1, self.v2)
        b = _side(self.v2, self.v3)
        c = _side(self.v3, self.v1)
        return a, b, c

    def perimeter(self) -> float:
        """Returns the perimeter."""
        return sum(self.side_lengths())

    def area(self) -> float:
        """Returns the area using Heron's formula."""
        a, b, c = self.side_lengths()
        s = (a + b + c) / 2
        return sqrt(s * (s - a) * (s - b) * (s - c))

    def is_equilateral(self, tol=1e-9) -> bool:
        """Returns True if all three sides are equal."""
        a, b, c = self.side_lengths()
        return abs(a - b) < tol and abs(b - c) < tol

    def is_isosceles(self, tol=1e-9) -> bool:
        """Returns True if at least two sides are equal."""
        a, b, c = self.side_lengths()
        return (abs(a - b) < tol or
                abs(b - c) < tol or
                abs(a - c) < tol)

    def is_right(self, tol=1e-9) -> bool:
        """Returns True if the triangle has a right angle (Pythagorean check)."""
        sides = sorted(self.side_lengths())
        a, b, c = sides
        return abs(a ** 2 + b ** 2 - c ** 2) < tol


    def draw(self, pen):
        """Draw the triangle."""
        _check_pen(pen)
        pen.stopDrawing()
        pen.tp(self.v1.x, self.v1.y)
        pen.startDrawing()
        pen.tp(self.v2.x, self.v2.y)   
        pen.tp(self.v3.x, self.v3.y)
        pen.tp(self.v1.x, self.v1.y)




class Square:
    """
    Axis-aligned square defined by its side length.
    For a rotated square use VertexSquare.
    """
    def __init__(self, side: float):
        self.side = side

    def __repr__(self):
        return f"Square(side={self.side})"

    # ── math ──
    def area(self) -> float:
        """Returns the area."""
        return self.side ** 2

    def perimeter(self) -> float:
        """Returns the perimeter."""
        return 4 * self.side

    def diagonal(self) -> float:
        """Returns the length of a diagonal."""
        return self.side * sqrt(2)

    # ── draw ──
    def draw(self, pen):
        """Draw the square."""
        _check_pen(pen)
        pen.startDrawing()             
        for _ in range(4):
            pen.move(self.side)
            pen.rotate(90)




class VertexSquare:
    """
    Square (or any quadrilateral) defined by 4 explicit vertices.
    Better for rotated or skewed squares.
    """
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, v4: Vertex):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4

    def __repr__(self):
        return f"VertexSquare({self.v1}, {self.v2}, {self.v3}, {self.v4})"

    
    def side_lengths(self) -> tuple:
        """Returns the four side lengths."""
        return (_side(self.v1, self.v2),
                _side(self.v2, self.v3),
                _side(self.v3, self.v4),
                _side(self.v4, self.v1))

    def perimeter(self) -> float:
        """Returns the perimeter."""
        return sum(self.side_lengths())

    def area(self) -> float:
        """
        Returns the area using the Shoelace formula.
        Works for any non-self-intersecting quadrilateral.
        """
        verts = [self.v1, self.v2, self.v3, self.v4]
        n = len(verts)
        total = 0.0
        for i in range(n):
            j = (i + 1) % n
            total += verts[i].x * verts[j].y
            total -= verts[j].x * verts[i].y
        return abs(total) / 2

    
    def draw(self, pen):
        """Draw the vertex-defined square."""
        _check_pen(pen)
        pen.stopDrawing()
        pen.tp(self.v1.x, self.v1.y)
        pen.startDrawing()
        pen.tp(self.v2.x, self.v2.y)
        pen.tp(self.v3.x, self.v3.y)
        pen.tp(self.v4.x, self.v4.y)
        pen.tp(self.v1.x, self.v1.y)



class Rectangle:
    """Axis-aligned rectangle defined by its width and height."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Rectangle(width={self.width}, height={self.height})"

    def area(self) -> float:
        """Returns the area."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Returns the perimeter."""
        return 2 * (self.width + self.height)

    def diagonal(self) -> float:
        """Returns the length of a diagonal."""
        return sqrt(self.width ** 2 + self.height ** 2)

    def draw(self, pen):
        """Draw the rectangle."""
        _check_pen(pen)
        pen.startDrawing()
        sides = [self.width, self.height, self.width, self.height]
        for side in sides:
            pen.move(side)
            pen.rotate(90)




class Ellipse:
    """
    Ellipse defined by its center vertex and semi-axes a (horizontal)
    and b (vertical).
    """

    def __init__(self, center: Vertex, a: float, b: float):
        if not isinstance(center, Vertex):
            raise TypeError("PYPEN ERR: center must be a Vertex.")
        self.center = center
        self.a = a   # semi-major axis
        self.b = b   # semi-minor axis

    def __repr__(self):
        return (f"Ellipse(center={self.center}, a={self.a}, b={self.b})")

    def area(self) -> float:
        """Returns the ellipse's area."""
        return pi * self.a * self.b

    def approx_perimeter(self) -> float:
        """
        Returns an approximation of the ellipse's perimeter
        using Ramanujan's formula.
        """
        h = ((self.a - self.b) ** 2) / ((self.a + self.b) ** 2)
        return pi * (self.a + self.b) * (1 + (3 * h) / (10 + sqrt(4 - 3 * h)))

    def contains_point(self, vertex: Vertex) -> bool:
        """Returns True if *vertex* lies inside (or on) the ellipse."""
        dx = (vertex.x - self.center.x) / self.a
        dy = (vertex.y - self.center.y) / self.b
        return dx * dx + dy * dy <= 1

    def draw(self, pen, steps=72, color="black", fill=False):
        """
        Draw the ellipse by approximating it with *steps* line segments.
        """
        _check_pen(pen)
        import math
        if fill:
            pen.initFill(color)
        pen.stopDrawing()
        start_x = self.center.x + self.a
        start_y = self.center.y
        pen.tp(start_x, start_y)
        pen.startDrawing()
        for i in range(1, steps + 1):
            angle = 2 * math.pi * i / steps
            x = self.center.x + self.a * math.cos(angle)
            y = self.center.y + self.b * math.sin(angle)
            pen.tp(x, y)
        if fill:
            pen.endFill()



class RegularPolygon:
    """
    A regular n-sided polygon defined by the number of sides and side length.
    """

    def __init__(self, sides: int, side_length: float):
        if sides < 3:
            raise ValueError("A polygon must have at least 3 sides.")
        self.sides = sides
        self.side_length = side_length

    def __repr__(self):
        return f"RegularPolygon(sides={self.sides}, side_length={self.side_length})"

    def perimeter(self) -> float:
        """Returns the perimeter."""
        return self.sides * self.side_length

    def area(self) -> float:
        """Returns the area."""
        return (self.sides * self.side_length ** 2) / (4 * tan(pi / self.sides))

    def interior_angle(self) -> float:
        """Returns one interior angle in degrees."""
        return (self.sides - 2) * 180 / self.sides

    def apothem(self) -> float:
        """Returns the apothem (radius of the inscribed circle)."""
        return self.side_length / (2 * tan(pi / self.sides))

    def circumradius(self) -> float:
        """Returns the circumradius (radius of the circumscribed circle)."""
        return self.side_length / (2 * (pi / self.sides) ** 0.5
                                   * (pi / self.sides) ** 0.5
                                   * 2 * tan(pi / self.sides) ** 0.5)
        # simpler formula:
        # return self.side_length / (2 * sin(pi / self.sides))

    def draw(self, pen):
        """Draw the regular polygon."""
        _check_pen(pen)
        exterior = 360 / self.sides
        pen.startDrawing()
        for _ in range(self.sides):
            pen.move(self.side_length)
            pen.rotate(exterior)




class Line:
    """A line segment between two vertices."""

    def __init__(self, start: Vertex, end: Vertex):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Line({self.start} -> {self.end})"

    def length(self) -> float:
        """Returns the length of the line segment."""
        return _side(self.start, self.end)

    def midpoint(self) -> Vertex:
        """Returns the midpoint as a Vertex."""
        mx = (self.start.x + self.end.x) / 2
        my = (self.start.y + self.end.y) / 2
        return Vertex(mx, my)

    def slope(self) -> float:
        """
        Returns the slope of the line.
        Raises ZeroDivisionError if the line is vertical.
        """
        dx = self.end.x - self.start.x
        if dx == 0:
            raise ZeroDivisionError("Line is vertical; slope is undefined.")
        return (self.end.y - self.start.y) / dx

    def draw(self, pen):
        """Draw the line segment."""
        _check_pen(pen)
        pen.stopDrawing()
        pen.tp(self.start.x, self.start.y)
        pen.startDrawing()
        pen.tp(self.end.x, self.end.y)




class Polygon:
    """
    A polygon defined by an arbitrary list of vertices.
    Use Triangle, Square, or RegularPolygon for common shapes.
    """

    def __init__(self, vertices: list):
        if len(vertices) < 3:
            raise ValueError("A polygon needs at least 3 vertices.")
        self.vertices = vertices

    def __repr__(self):
        return f"Polygon({self.vertices})"

    def perimeter(self) -> float:
        """Returns the perimeter."""
        total = 0.0
        n = len(self.vertices)
        for i in range(n):
            total += _side(self.vertices[i], self.vertices[(i + 1) % n])
        return total

    def area(self) -> float:
        """Returns the area using the Shoelace formula."""
        n = len(self.vertices)
        total = 0.0
        for i in range(n):
            j = (i + 1) % n
            total += self.vertices[i].x * self.vertices[j].y
            total -= self.vertices[j].x * self.vertices[i].y
        return abs(total) / 2

    def draw(self, pen):
        """Draw the polygon."""
        _check_pen(pen)
        pen.stopDrawing()
        pen.tp(self.vertices[0].x, self.vertices[0].y)
        pen.startDrawing()
        for v in self.vertices[1:]:
            pen.tp(v.x, v.y)
        pen.tp(self.vertices[0].x, self.vertices[0].y)