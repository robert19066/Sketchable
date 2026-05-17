"""
licenced under the MIT licence
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

Changelog - V1.4:
- All vertex-based shapes (Line, Triangle, CustomSquare, Mesh) now accept either
  individual Vertex arguments OR a single Cluster, making them fully Cluster-compatible.
- Mesh now stores vertices in a Cluster internally; get_cluster() exposes it.
- Fixed Circle.getX/getY/contains_point using dead getvX()/getvY() — now use .x/.y.
- Fixed Mesh.__repr__ incorrectly saying "Polygon".
- Removed duplicate imports (cos, sin, radians were imported three times).
- Cluster gains from_list() classmethod and __len__/__iter__ for convenience.
- Fixed collision logic and gave _Moveable some love and care after so much time.(it got last updated in v1.2.0)
"""

from math import pi, sqrt, tan, cos, sin, radians
from typing import List, Tuple


# ── helpers ───────────────────────────────────────────────────────────────────

def _side(a, b) -> float:
    """Euclidean distance between two Vertex objects."""
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


# ── Moveable ──────────────────────────────────────────────────────────────────

class _Moveable:
    """Helper class for tracking and applying spatial transformations.
    TO NOTE: vx and vy are the shape's coordinates.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        # We store the base (local) coordinates right inside the moveable object
        self._base_pos = (float(x), float(y))
        self._pos   = (0.0, 0.0)
        self._angle = 0.0          # degrees, CCW
        self._scale = 1.0

    # ── position ──
    def move_to(self, x: float, y: float) -> "_Moveable":
        """Set world offset position to absolute (x, y)."""
        self._pos = (float(x), float(y))
        return self

    def move_by(self, dx: float, dy: float) -> "_Moveable":
        """Shift current world offset by (dx, dy)."""
        self._pos = (self._pos[0] + dx, self._pos[1] + dy)
        return self

    # ── rotation ──
    def rotate_to(self, angle: float) -> "_Moveable":
        self._angle = angle % 360
        return self

    def rotate_by(self, delta: float) -> "_Moveable":
        self._angle = (self._angle + delta) % 360
        return self

    # ── scale ──
    def set_scale(self, factor: float) -> "_Moveable":
        if factor <= 0:
            raise ValueError("Scale must be positive.")
        self._scale = factor
        return self

    def scale_by(self, factor: float) -> "_Moveable":
        if factor <= 0:
            raise ValueError("Scale must be positive.")
        self._scale *= factor
        return self

    def reset_transform(self) -> "_Moveable":
        self._pos   = (0.0, 0.0)
        self._angle = 0.0
        self._scale = 1.0
        return self

    # ── Transforming Coordinates ──
    @property
    def transformed_position(self) -> Tuple[float, float]:
        """Calculates the absolute world position after Scale -> Rotate -> Translate."""
        rad = radians(self._angle)
        c, s = cos(rad), sin(rad)
        tx, ty = self._pos

        # Apply transforms to the base position
        x = self._base_pos[0] * self._scale
        y = self._base_pos[1] * self._scale

        world_x = x * c - y * s + tx
        world_y = x * s + y * c + ty
        return (world_x, world_y)
    
    def _apply_transform(self, vertices):
        """
        Apply transform only to local coordinate tuples.
        Vertex-based shapes already provide world coords.
        """
        if not vertices:
            return []

        # already world coordinates
        if isinstance(vertices[0], Vertex):
            return [(v.x, v.y) for v in vertices]

        rad = radians(self._angle)
        c, s = cos(rad), sin(rad)

        transformed = []

        for x, y in vertices:
            # scale
            x *= self._scale
            y *= self._scale

            # rotate
            rx = x * c - y * s
            ry = x * s + y * c

            # translate
            rx += self._pos[0]
            ry += self._pos[1]

            transformed.append((rx, ry))

        return transformed


# ── Vertex ────────────────────────────────────────────────────────────────────

class Vertex(_Moveable):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def __repr__(self):
        wx, wy = self.transformed_position
        return f"Vertex(world_x={wx:.2f}, world_y={wy:.2f})"

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        return self.transformed_position == other.transformed_position

    # Pythonic alternative to getvX / getvY
    @property
    def x(self) -> float:
        return self.transformed_position[0]

    @property
    def y(self) -> float:
        return self.transformed_position[1]


# ── Cluster ───────────────────────────────────────────────────────────────────

class Cluster:
    """An ordered collection of Vertex objects.

    Accepted anywhere a sequence of vertices is needed. All vertex-based shapes
    can be constructed directly from a Cluster instead of individual Vertex args.
    """

    def __init__(self):
        self.vertexes: List[Vertex] = []

    # ── construction helpers ──
    @classmethod
    def from_list(cls, vertices: List[Vertex]) -> "Cluster":
        """Create a Cluster pre-populated from a list of Vertex objects."""
        c = cls()
        for v in vertices:
            c.add(v)
        return c

    # ── collection protocol ──
    def __len__(self) -> int:
        return len(self.vertexes)

    def __iter__(self):
        return iter(self.vertexes)

    def __getitem__(self, index: int) -> Vertex:
        return self.vertexes[index]

    # ── mutation ──
    def add(self, vertex: Vertex):
        """Append a Vertex to the cluster."""
        if not isinstance(vertex, Vertex):
            raise TypeError("Can only add Vertex instances to Cluster.")
        self.vertexes.append(vertex)

    def remove(self, index: int):
        """Delete the vertex at *index* (no return value)."""
        del self.vertexes[index]

    def pop(self, index: int) -> Vertex:
        """Remove and return the vertex at *index*."""
        return self.vertexes.pop(index)

    def shift_to(self, index: int, vx: float, vy: float):
        """Set vertex at *index* to absolute world position (vx, vy)."""
        self.vertexes[index].move_to(vx, vy)

    def shift_by(self, index: int, vx: float, vy: float):
        """Offset vertex at *index* by (vx, vy)."""
        self.vertexes[index].move_by(vx, vy)


# ── internal helper ───────────────────────────────────────────────────────────

def _require_vertex(v, name: str) -> Vertex:
    """Raise a clear error when a positional arg is not a Vertex."""
    if not isinstance(v, Vertex):
        raise TypeError(f"{name} must be a Vertex, got {type(v).__name__}.")
    return v


def _cluster_or_vertices(first, rest, min_count: int, shape_name: str) -> List[Vertex]:
    """Return a flat list of Vertex objects from either:
      - a single Cluster  (first=Cluster, rest=())
      - individual Vertex args (first=Vertex, rest=(Vertex, ...))

    Raises ValueError when fewer than *min_count* vertices are supplied.
    """
    if isinstance(first, Cluster):
        if rest:
            raise TypeError(
                f"{shape_name}: pass either a Cluster OR individual Vertex args, not both."
            )
        verts = list(first)
    else:
        verts = [_require_vertex(first, "first vertex")] + [
            _require_vertex(v, f"vertex {i+2}") for i, v in enumerate(rest)
        ]
    if len(verts) < min_count:
        raise ValueError(
            f"{shape_name} needs at least {min_count} vertices, got {len(verts)}."
        )
    return verts


# ── Line ──────────────────────────────────────────────────────────────────────

class Line(_Moveable):
    """A line segment between two vertices.

    Constructors
    ------------
    Line(start, end)           – two Vertex objects
    Line(cluster)              – Cluster with exactly 2 vertices
    """

    def __init__(self, start_or_cluster, end: Vertex = None):
        super().__init__()
        if isinstance(start_or_cluster, Cluster):
            if end is not None:
                raise TypeError("Line: pass either a Cluster OR two Vertex args, not both.")
            verts = _cluster_or_vertices(start_or_cluster, (), 2, "Line")
            if len(verts) != 2:
                raise ValueError(f"Line needs exactly 2 vertices, got {len(verts)}.")
            self.start, self.end = verts[0], verts[1]
        else:
            self.start = _require_vertex(start_or_cluster, "start")
            self.end   = _require_vertex(end, "end")

    def __repr__(self):
        return f"Line({self.start} -> {self.end})"

    def get_cluster(self) -> Cluster:
        """Return the two endpoints as a Cluster."""
        return Cluster.from_list([self.start, self.end])

    def get_vertices(self) -> list:
        """Lines are open — no closing point added."""
        return [self.start, self.end]

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
    """Circle defined by a centre Vertex and a radius.

    Note: Circle is not vertex-based in the same sense as the polygon shapes,
    so it does not support Cluster construction.
    """

    def __init__(self, center: Vertex, radius: float):
        if not isinstance(center, Vertex):
            raise TypeError("center must be a Vertex.")
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius})"

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return False
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
    def getX(self) -> float:      return self.center.x
    def getY(self) -> float:      return self.center.y
    def getRadius(self) -> float: return self.radius

    # ── math ──
    def area(self) -> float:   return pi * self.radius ** 2
    def circ(self) -> float:   return 2 * pi * self.radius
    def diam(self) -> float:   return self.radius * 2

    def contains_point(self, vertex: Vertex) -> bool:
        dx = vertex.x - self.center.x
        dy = vertex.y - self.center.y
        return dx * dx + dy * dy <= self.radius ** 2


# ── Triangle ──────────────────────────────────────────────────────────────────

class Triangle(_Moveable):
    """Triangle defined by three vertices.

    Constructors
    ------------
    Triangle(v1, v2, v3)   – three Vertex objects
    Triangle(cluster)      – Cluster with exactly 3 vertices
    """

    def __init__(self, v1_or_cluster, v2: Vertex = None, v3: Vertex = None):
        super().__init__()
        verts = _cluster_or_vertices(v1_or_cluster, [v for v in (v2, v3) if v is not None], 3, "Triangle")
        if len(verts) != 3:
            raise ValueError(f"Triangle needs exactly 3 vertices, got {len(verts)}.")
        self.v1, self.v2, self.v3 = verts

    def __repr__(self):
        return f"Triangle({self.v1}, {self.v2}, {self.v3})"

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return self.v1 == other.v1 and self.v2 == other.v2 and self.v3 == other.v3

    def get_cluster(self) -> Cluster:
        """Return the three vertices as a Cluster."""
        return Cluster.from_list([self.v1, self.v2, self.v3])

    def get_vertices(self) -> list:
        return [self.v1, self.v2, self.v3]

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
    Use Movement to position it in the world.

    Note: Square is side-length-based, not vertex-based. Use CustomSquare if
    you need to define corners explicitly with Vertex objects or a Cluster.
    """

    def __init__(self, side: float):
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


# ── CustomSquare ──────────────────────────────────────────────────────────────

class CustomSquare(_Moveable):
    """Quadrilateral defined by 4 explicit vertices (supports rotation/skew).

    Constructors
    ------------
    CustomSquare(v1, v2, v3, v4)   – four Vertex objects
    CustomSquare(cluster)          – Cluster with exactly 4 vertices
    """

    def __init__(self, v1_or_cluster, v2: Vertex = None,
                 v3: Vertex = None, v4: Vertex = None):
        super().__init__()
        rest = [v for v in (v2, v3, v4) if v is not None]
        verts = _cluster_or_vertices(v1_or_cluster, rest, 4, "CustomSquare")
        if len(verts) != 4:
            raise ValueError(f"CustomSquare needs exactly 4 vertices, got {len(verts)}.")
        self.v1, self.v2, self.v3, self.v4 = verts

    def __repr__(self):
        return f"CustomSquare({self.v1}, {self.v2}, {self.v3}, {self.v4})"

    def get_cluster(self) -> Cluster:
        """Return the four vertices as a Cluster."""
        return Cluster.from_list([self.v1, self.v2, self.v3, self.v4])

    def get_vertices(self) -> list:
        return [self.v1,self.v2,self.v3,self.v4]

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


# ── SidePolygon ───────────────────────────────────────────────────────────────

class SidePolygon(_Moveable):
    """Regular n-sided polygon. Vertices generated around local origin (0, 0).
    Use Movement to position it in the world.

    Note: SidePolygon is side-count/length-based, not vertex-based. Use Mesh
    if you need to define corners explicitly with Vertex objects or a Cluster.
    """

    def __init__(self, sides: int, side_length: float):
        super().__init__()
        if sides < 3:
            raise ValueError("A polygon needs at least 3 sides.")
        self.sides       = sides
        self.side_length = side_length

    def __repr__(self):
        return f"SidePolygon(sides={self.sides}, side_length={self.side_length})"

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


# ── Mesh ──────────────────────────────────────────────────────────────────────

class Mesh(_Moveable):
    """Arbitrary closed polygon from an explicit list of Vertex objects or a Cluster.

    Constructors
    ------------
    Mesh([v1, v2, v3, ...])   – list of Vertex objects (3 or more)
    Mesh(cluster)             – a Cluster (3 or more vertices)

    Vertices are stored internally as a Cluster. Use get_cluster() to retrieve it.
    """

    def __init__(self, vertices):
        super().__init__()
        if isinstance(vertices, Cluster):
            cluster = vertices
        elif isinstance(vertices, list):
            cluster = Cluster.from_list(vertices)
        else:
            raise TypeError(
                "Mesh expects a list of Vertex objects or a Cluster, "
                f"got {type(vertices).__name__}."
            )
        if len(cluster) < 3:
            raise ValueError("A Mesh needs at least 3 vertices.")
        self._cluster = cluster

    def __repr__(self):
        return f"Mesh({list(self._cluster.vertexes)})"

    def get_cluster(self) -> Cluster:
        """Return the internal Cluster (live reference — mutations affect the Mesh)."""
        return self._cluster

    def get_vertices(self) -> list:
        return list(self._cluster)

    # ── math ──
    def perimeter(self) -> float:
        verts = self._cluster.vertexes
        n = len(verts)
        return sum(_side(verts[i], verts[(i+1) % n]) for i in range(n))

    def area(self) -> float:
        verts = self._cluster.vertexes
        n = len(verts)
        total = sum(verts[i].x * verts[(i+1)%n].y -
                    verts[(i+1)%n].x * verts[i].y for i in range(n))
        return abs(total) / 2