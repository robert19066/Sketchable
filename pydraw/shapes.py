
"""
licenced under the GNU Affero General Public License v3.0 (AGPL3)
This file is used for all the datatypes.

This code was written mostly by me, yet I used AI to add math to Triangle, Square and VertexSquare. Also I used it for function descriptions. Rest of the logic was made by me.
Yes, it defies the "no ai" rule, BUT i didn't vibe code, i just used it to tidy up my code, and eliminate inconsistencies across all shapes. 

Yes but you mind ask, "BUT YOU DON'T KNOW GEOMETRY?!". dumbasses i am 6th grade HOW THE FUQ I AM SUPPOSED TO KNOW SHOELACE FORMULA?!
or the other complicated shi.
So please, no hate. Trying to quit vibe coding.

Changelog - V1.3:
- Made Moveble an helper class for motion.py's Motion class(more intuitive.)

Changelog - V1.3 (crittical bugfix):
- All _Moveable subclasses now call super().__init__() so _pos, _angle, _scale
  are always initialised. Previously only Square did this, so move_by/rotate_to
  etc. would crash on Triangle, Line, VertexSquare, RegularPolygon and Polygon.
"""

from math import pi, sqrt, tan, cos, sin, radians


# ── helpers ───────────────────────────────────────────────────────────────────

def _side(a, b) -> float:
    """Euclidean distance between two Vertex objects."""
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


# ── Moveable ──────────────────────────────────────────────────────────────────

class _Moveable:
    """
    Helper class for the new Motion class.
    """

    def __init__(self):
        self._pos   = (0.0, 0.0)
        self._angle = 0.0          # degrees, CCW
        self._scale = 1.0

    # ── position ──
    def move_to(self, x: float, y: float) -> "_Moveable":
        """Set world position to absolute (x, y)."""
        self._pos = (float(x), float(y))
        return self

    def move_by(self, dx: float, dy: float) -> "_Moveable":
        """Shift current position by (dx, dy)."""
        self._pos = (self._pos[0] + dx, self._pos[1] + dy)
        return self

    # ── rotation ──
    def rotate_to(self, angle: float) -> "_Moveable":
        """Set rotation to an absolute angle in degrees (CCW)."""
        self._angle = angle % 360
        return self

    def rotate_by(self, delta: float) -> "_Moveable":
        """Add delta degrees (CCW) to current rotation."""
        self._angle = (self._angle + delta) % 360
        return self

    # ── scale ──
    def set_scale(self, factor: float) -> "_Moveable":
        """Set uniform scale (1.0 = original size)."""
        if factor <= 0:
            raise ValueError("Scale must be positive.")
        self._scale = factor
        return self

    def scale_by(self, factor: float) -> "_Moveable":
        """Multiply current scale by factor."""
        if factor <= 0:
            raise ValueError("Scale must be positive.")
        self._scale *= factor
        return self

    # ── reset ──
    def reset_transform(self) -> "_Moveable":
        """Reset position, rotation, and scale to defaults."""
        self._pos   = (0.0, 0.0)
        self._angle = 0.0
        self._scale = 1.0
        return self

    # ── getters ──
    @property
    def position(self) -> tuple: return self._pos

    @property
    def angle(self) -> float:
        return self._angle

    @property
    def scale(self) -> float: return self._scale

    # ── transform ──
    def _apply_transform(self, pts: list) -> list:
        """Apply Scale → Rotate → Translate to a list of (x, y) tuples."""
        rad  = radians(self._angle)
        c, s = cos(rad), sin(rad)
        tx, ty = self._pos
        result = []
        for (x, y) in pts:
            x *= self._scale
            y *= self._scale
            result.append((x * c - y * s + tx,
                           x * s + y * c + ty))
        return result


# ── Vertex ────────────────────────────────────────────────────────────────────

class Vertex(_Moveable):
    def __init__(self, x: float, y: float):
        super().__init__()          # ← bugfix: was missing
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vertex(x={self.x}, y={self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def getvX(self): return self.x
    def getvY(self): return self.y


# ── Line ──────────────────────────────────────────────────────────────────────

class Line(_Moveable):
    """A line segment between two vertices."""

    def __init__(self, start: Vertex, end: Vertex):
        super().__init__()          # ← bugfix: was missing
        self.start = start
        self.end   = end

    def __repr__(self):
        return f"Line({self.start} -> {self.end})"

    def get_vertices(self) -> list:
        # Lines are open — no closing point added.
        return [(self.start.x, self.start.y),
                (self.end.x,   self.end.y)]

    # ── math ──
    def length(self) -> float:
        return _side(self.start, self.end)

    def midpoint(self) -> Vertex:
        return Vertex((self.start.x + self.end.x) / 2,
                      (self.start.y + self.end.y) / 2)

    def slope(self) -> float:
        dx = self.end.x - self.start.x
        if dx == 0:
            raise ZeroDivisionError("Line is vertical — slope undefined.")
        return (self.end.y - self.start.y) / dx


# ── Circle ────────────────────────────────────────────────────────────────────

class Circle:
    def __init__(self, center: Vertex, radius: float):
        if not isinstance(center, Vertex):
            raise TypeError("center must be a Vertex.")
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius})"

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius

    def get_vertices(self, steps: int = 72) -> list:
        """Approximate the circle as *steps* points (closed)."""
        pts = []
        for i in range(steps + 1):
            a = 2 * pi * i / steps
            pts.append((self.center.x + self.radius * cos(a),
                        self.center.y + self.radius * sin(a)))
        return pts

    # ── getters ──
    def getX(self):      return self.center.getvX()
    def getY(self):      return self.center.getvY()
    def getRadius(self): return self.radius

    # ── math ──
    def area(self) -> float:   return pi * self.radius ** 2
    def circ(self) -> float:   return 2 * pi * self.radius
    def diam(self) -> float:   return self.radius * 2

    def contains_point(self, vertex: Vertex) -> bool:
        dx = vertex.getvX() - self.center.getvX()
        dy = vertex.getvY() - self.center.getvY()
        return dx * dx + dy * dy <= self.radius ** 2


# ── Triangle ──────────────────────────────────────────────────────────────────

class Triangle(_Moveable):
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex):
        super().__init__()          # ← bugfix: was missing
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def __repr__(self):
        return f"Triangle({self.v1}, {self.v2}, {self.v3})"

    def __eq__(self, other):
        return self.v1 == other.v1 and self.v2 == other.v2 and self.v3 == other.v3

    def get_vertices(self) -> list:
        return [(self.v1.x, self.v1.y),
                (self.v2.x, self.v2.y),
                (self.v3.x, self.v3.y)]

    # ── math ──
    def side_lengths(self) -> tuple:
        return (_side(self.v1, self.v2),
                _side(self.v2, self.v3),
                _side(self.v3, self.v1))

    def perimeter(self) -> float:
        return sum(self.side_lengths())

    def area(self) -> float:
        a, b, c = self.side_lengths()
        s = (a + b + c) / 2
        return sqrt(s * (s - a) * (s - b) * (s - c))

    def is_equilateral(self, tol=1e-9) -> bool:
        a, b, c = self.side_lengths()
        return abs(a - b) < tol and abs(b - c) < tol

    def is_isosceles(self, tol=1e-9) -> bool:
        a, b, c = self.side_lengths()
        return abs(a - b) < tol or abs(b - c) < tol or abs(a - c) < tol

    def is_right(self, tol=1e-9) -> bool:
        a, b, c = sorted(self.side_lengths())
        return abs(a ** 2 + b ** 2 - c ** 2) < tol


# ── Square ────────────────────────────────────────────────────────────────────

class Square(_Moveable):
    """Axis-aligned square. Vertices are generated from the local origin (0, 0).
    Use Movement to position it in the world."""

    def __init__(self, side):
        super().__init__()
        self.side = side

    def __repr__(self):
        return f"Square(side={self.side})"

    def get_vertices(self) -> list:
        s = self.side
        return [(0, 0), (s, 0), (s, s), (0, s)]

    # ── math ──
    def area(self) -> float:      return self.side ** 2
    def perimeter(self) -> float: return 4 * self.side
    def diagonal(self) -> float:  return self.side * sqrt(2)


# ── VertexSquare ──────────────────────────────────────────────────────────────

class VertexSquare(_Moveable):
    """Quadrilateral defined by 4 explicit vertices (supports rotation/skew)."""

    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, v4: Vertex):
        super().__init__()          # ← bugfix: was missing
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4

    def __repr__(self):
        return f"VertexSquare({self.v1}, {self.v2}, {self.v3}, {self.v4})"

    def get_vertices(self) -> list:
        return [(self.v1.x, self.v1.y), (self.v2.x, self.v2.y),
                (self.v3.x, self.v3.y), (self.v4.x, self.v4.y)]

    # ── math ──
    def side_lengths(self) -> tuple:
        return (_side(self.v1, self.v2), _side(self.v2, self.v3),
                _side(self.v3, self.v4), _side(self.v4, self.v1))

    def perimeter(self) -> float:
        return sum(self.side_lengths())

    def area(self) -> float:
        verts = [self.v1, self.v2, self.v3, self.v4]
        n = len(verts)
        total = sum(verts[i].x * verts[(i+1)%n].y -
                    verts[(i+1)%n].x * verts[i].y for i in range(n))
        return abs(total) / 2


# ── Ellipse ───────────────────────────────────────────────────────────────────

class Ellipse:
    """Ellipse defined by center Vertex, semi-axis a (horizontal), b (vertical)."""

    def __init__(self, center: Vertex, a: float, b: float):
        if not isinstance(center, Vertex):
            raise TypeError("center must be a Vertex.")
        self.center = center
        self.a = a
        self.b = b

    def __repr__(self):
        return f"Ellipse(center={self.center}, a={self.a}, b={self.b})"

    def get_vertices(self, steps: int = 72) -> list:
        """Approximate the ellipse as *steps* points (closed)."""
        pts = []
        for i in range(steps + 1):
            angle = 2 * pi * i / steps
            pts.append((self.center.x + self.a * cos(angle),
                        self.center.y + self.b * sin(angle)))
        return pts

    # ── math ──
    def area(self) -> float:
        return pi * self.a * self.b

    def approx_perimeter(self) -> float:
        """Ramanujan's approximation."""
        h = ((self.a - self.b) ** 2) / ((self.a + self.b) ** 2)
        return pi * (self.a + self.b) * (1 + (3 * h) / (10 + sqrt(4 - 3 * h)))

    def contains_point(self, vertex: Vertex) -> bool:
        dx = (vertex.x - self.center.x) / self.a
        dy = (vertex.y - self.center.y) / self.b
        return dx * dx + dy * dy <= 1


# ── RegularPolygon ────────────────────────────────────────────────────────────

class RegularPolygon(_Moveable):
    """Regular n-sided polygon. Vertices generated around local origin (0, 0).
    Use Movement to position it in the world."""

    def __init__(self, sides: int, side_length: float):
        super().__init__()          # ← bugfix: was missing
        if sides < 3:
            raise ValueError("A polygon needs at least 3 sides.")
        self.sides       = sides
        self.side_length = side_length

    def __repr__(self):
        return f"RegularPolygon(sides={self.sides}, side_length={self.side_length})"

    def get_vertices(self) -> list:
        """Vertices centred on the origin, first point at the top."""
        r = self.side_length / (2 * sin(pi / self.sides))
        pts = []
        for i in range(self.sides):
            angle = 2 * pi * i / self.sides - pi / 2
            pts.append((r * cos(angle), r * sin(angle)))
        return pts

    # ── math ──
    def perimeter(self) -> float:      return self.sides * self.side_length
    def interior_angle(self) -> float: return (self.sides - 2) * 180 / self.sides
    def apothem(self) -> float:        return self.side_length / (2 * tan(pi / self.sides))
    def area(self) -> float:
        return (self.sides * self.side_length ** 2) / (4 * tan(pi / self.sides))


# ── Polygon ───────────────────────────────────────────────────────────────────

class Polygon(_Moveable):
    """Arbitrary polygon from a list of Vertex objects."""

    def __init__(self, vertices: list):
        super().__init__()          # ← bugfix: was missing
        if len(vertices) < 3:
            raise ValueError("A polygon needs at least 3 vertices.")
        self.vertices = vertices

    def __repr__(self):
        return f"Polygon({self.vertices})"

    def get_vertices(self) -> list:
        return [(v.x, v.y) for v in self.vertices]

    # ── math ──
    def perimeter(self) -> float:
        n = len(self.vertices)
        return sum(_side(self.vertices[i], self.vertices[(i+1) % n])
                   for i in range(n))

    def area(self) -> float:
        verts = self.vertices
        n = len(verts)
        total = sum(verts[i].x * verts[(i+1)%n].y -
                    verts[(i+1)%n].x * verts[i].y for i in range(n))
        return abs(total) / 2