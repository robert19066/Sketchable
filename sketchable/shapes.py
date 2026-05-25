"""
licenced under the PMIT licence
This file is used for all the datatypes.

This code was written mostly by me, yet I used AI to add math to Triangle, Square and VertexSquare. Also I used it for function descriptions. Rest of the logic was made by me.


Changelog - V1.3.3:
- Made Moveble an helper class for motion.py's Motion class(more intuitive.)

Changelog - V1.3.4 (crittical bugfix):
- All _Moveable subclasses now call super().__init__() so _pos, _angle, _scale
  are always initialised. Previously only Square did this, so move_by/rotate_to
  etc. would crash on Triangle, Line, VertexSquare, RegularPolygon and Polygon.

Changelog - V1.3.5:
- All vertex-based shapes (Line, Triangle, CustomSquare, Mesh) now accept either
  individual Vertex arguments OR a single Cluster, making them fully Cluster-compatible.
- Mesh now stores vertices in a Cluster internally; get_cluster() exposes it.
- Fixed Circle.getX/getY/contains_point using dead getvX()/getvY() — now use .x/.y.
- Fixed Mesh.__repr__ incorrectly saying "Polygon".
- Removed duplicate imports (cos, sin, radians were imported three times).
- Cluster gains from_list() classmethod and __len__/__iter__ for convenience.
- Fixed collision logic and gave _Moveable some love and care after so much time.(it got last updated in v1.2.0)

Changelog - V1.3.6:
- Triangle gains getSideLength(va, vb), getAngle(dx1, dy1, dx2, dy2) (static),
  centroid(), circumradius(), inradius(), angles(), height_from(v),
  is_scalene(), is_obtuse(), is_acute().
- Circle gains sector_area(), arc_length(), chord_length() and now validates
  that radius > 0.
- Line gains angle(), y_intercept(), contains_point() and __eq__.
- Square gains __eq__, inscribed_radius(), circumscribed_radius().
- CustomSquare gains __eq__, diagonals().
- SidePolygon gains __eq__, circumradius(), diagonal_count().
- Mesh gains __eq__, centroid().
- All shapes: tightened type/value guards, consistent numeric-tolerance
  parameters, and full docstrings on every method.
- Added acos and degrees to math imports.
- Added new __eq__ methods to all shapes for easier testing and comparison.
- Triangle got an new __eq__ method, and all the math methods now guard against floating-point. Its way better than the old vertex-based one, and it will work in all cases.
"""

from math import pi, sqrt, tan, cos, sin, radians, acos, degrees
from typing import List, Tuple


# ── helpers ───────────────────────────────────────────────────────────────────

def _side(a, b) -> float:
    """Return the Euclidean distance between two Vertex objects."""
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


def _clamp(value: float, lo: float, hi: float) -> float:
    """Clamp *value* to [lo, hi]. Used to guard acos against float rounding."""
    return max(lo, min(hi, value))


# ── Moveable ──────────────────────────────────────────────────────────────────

class _Moveable:
    """Helper mixin that tracks and applies spatial transformations.

    Subclasses call ``super().__init__(x, y)`` to set a base (local) position.
    The world position is computed lazily via ``transformed_position``.

    Note
    ----
    ``vx`` and ``vy`` are the shape's *local* coordinates; the actual world
    position accounts for scale, rotation, and translation.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self._base_pos = (float(x), float(y))
        self._pos      = (0.0, 0.0)  # world-space translation offset
        self._angle    = 0.0          # rotation in degrees, CCW
        self._scale    = 1.0

    # ── position ──────────────────────────────────────────────────────────────

    def move_to(self, x: float, y: float) -> "_Moveable":
        """Set the world-offset position to the absolute coordinates (x, y)."""
        self._pos = (float(x), float(y))
        return self

    def move_by(self, dx: float, dy: float) -> "_Moveable":
        """Shift the current world offset by (dx, dy)."""
        self._pos = (self._pos[0] + dx, self._pos[1] + dy)
        return self

    # ── rotation ──────────────────────────────────────────────────────────────

    def rotate_to(self, angle: float) -> "_Moveable":
        """Set the rotation to *angle* degrees (CCW). Value is wrapped to [0, 360)."""
        self._angle = float(angle) % 360
        return self

    def rotate_by(self, delta: float) -> "_Moveable":
        """Add *delta* degrees (CCW) to the current rotation."""
        self._angle = (self._angle + float(delta)) % 360
        return self

    # ── scale ─────────────────────────────────────────────────────────────────

    def set_scale(self, factor: float) -> "_Moveable":
        """Set the uniform scale to *factor*. Must be strictly positive."""
        if factor <= 0:
            raise ValueError(f"Scale must be positive, got {factor}.")
        self._scale = float(factor)
        return self

    def scale_by(self, factor: float) -> "_Moveable":
        """Multiply the current scale by *factor*. Must be strictly positive."""
        if factor <= 0:
            raise ValueError(f"Scale factor must be positive, got {factor}.")
        self._scale *= float(factor)
        return self

    def reset_transform(self) -> "_Moveable":
        """Reset translation, rotation, and scale back to their defaults."""
        self._pos   = (0.0, 0.0)
        self._angle = 0.0
        self._scale = 1.0
        return self

    # ── world-space helpers ───────────────────────────────────────────────────

    @property
    def transformed_position(self) -> Tuple[float, float]:
        """Absolute world position after applying Scale → Rotate → Translate."""
        rad = radians(self._angle)
        c, s = cos(rad), sin(rad)
        tx, ty = self._pos

        x = self._base_pos[0] * self._scale
        y = self._base_pos[1] * self._scale

        world_x = x * c - y * s + tx
        world_y = x * s + y * c + ty
        return (world_x, world_y)

    def _apply_transform(self, vertices) -> list:
        """Apply the stored transform to a sequence of local-coordinate tuples.

        Vertex objects are returned as-is (they already carry world coords);
        plain ``(x, y)`` tuples are scaled, rotated, and translated.
        """
        if not vertices:
            return []

        if isinstance(vertices[0], Vertex):
            return [(v.x, v.y) for v in vertices]

        rad = radians(self._angle)
        c, s = cos(rad), sin(rad)

        transformed = []
        for x, y in vertices:
            x *= self._scale
            y *= self._scale
            rx = x * c - y * s + self._pos[0]
            ry = x * s + y * c + self._pos[1]
            transformed.append((rx, ry))
        return transformed


# ── Vertex ────────────────────────────────────────────────────────────────────

class Vertex(_Moveable):
    """A 2-D point in world space.

    Inherits from ``_Moveable`` so vertices can be translated, rotated, and
    scaled independently, which is useful when animating individual corners.

    Parameters
    ----------
    x, y : float
        Initial local coordinates.

    Properties
    ----------
    x : float
        World-space X coordinate (read-only; reflects all transforms).
    y : float
        World-space Y coordinate (read-only; reflects all transforms).
    """

    def __init__(self, x: float, y: float):
        super().__init__(float(x), float(y))

    def __repr__(self) -> str:
        wx, wy = self.transformed_position
        return f"Vertex(world_x={wx:.2f}, world_y={wy:.2f})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vertex):
            return False
        return self.transformed_position == other.transformed_position

    @property
    def x(self) -> float:
        """World-space X coordinate."""
        return self.transformed_position[0]

    @property
    def y(self) -> float:
        """World-space Y coordinate."""
        return self.transformed_position[1]


# ── Cluster ───────────────────────────────────────────────────────────────────

class Cluster:
    """An ordered, mutable collection of :class:`Vertex` objects.

    Accepted anywhere a sequence of vertices is required. All vertex-based
    shapes can be constructed directly from a Cluster instead of individual
    Vertex arguments.

    Examples
    --------
    >>> c = Cluster.from_list([Vertex(0, 0), Vertex(1, 0), Vertex(0, 1)])
    >>> Triangle(c)
    """

    def __init__(self):
        self.vertexes: List[Vertex] = []

    # ── construction helpers ──────────────────────────────────────────────────

    @classmethod
    def from_list(cls, vertices: List[Vertex]) -> "Cluster":
        """Create a Cluster pre-populated from a list of Vertex objects."""
        c = cls()
        for v in vertices:
            c.add(v)
        return c

    # ── collection protocol ───────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self.vertexes)

    def __iter__(self):
        return iter(self.vertexes)

    def __getitem__(self, index: int) -> Vertex:
        return self.vertexes[index]

    def __repr__(self) -> str:
        return f"Cluster({self.vertexes})"

    # ── mutation ──────────────────────────────────────────────────────────────

    def add(self, vertex: Vertex):
        """Append *vertex* to the end of the cluster."""
        if not isinstance(vertex, Vertex):
            raise TypeError(
                f"Cluster.add expects a Vertex, got {type(vertex).__name__}."
            )
        self.vertexes.append(vertex)

    def remove(self, index: int):
        """Delete the vertex at *index* (no return value)."""
        del self.vertexes[index]

    def pop(self, index: int) -> Vertex:
        """Remove and return the vertex at *index*."""
        return self.vertexes.pop(index)

    def shift_to(self, index: int, vx: float, vy: float):
        """Move the vertex at *index* to absolute world position (vx, vy)."""
        self.vertexes[index].move_to(vx, vy)

    def shift_by(self, index: int, vx: float, vy: float):
        """Offset the vertex at *index* by (vx, vy)."""
        self.vertexes[index].move_by(vx, vy)


# ── internal helpers ──────────────────────────────────────────────────────────

def _require_vertex(v, name: str) -> Vertex:
    """Raise a clear :class:`TypeError` when a positional arg is not a Vertex."""
    if not isinstance(v, Vertex):
        raise TypeError(f"{name} must be a Vertex, got {type(v).__name__}.")
    return v


def _cluster_or_vertices(first, rest, min_count: int, shape_name: str) -> List[Vertex]:
    """Return a flat list of Vertex objects from either:

    - a single :class:`Cluster` (``first=Cluster``, ``rest=()``)
    - individual :class:`Vertex` args (``first=Vertex``, ``rest=(Vertex, ...)``)

    Raises
    ------
    TypeError
        If both a Cluster *and* individual Vertex args are supplied.
    ValueError
        If fewer than *min_count* vertices are provided.
    """
    if isinstance(first, Cluster):
        if rest:
            raise TypeError(
                f"{shape_name}: pass either a Cluster OR individual Vertex args, not both."
            )
        verts = list(first)
    else:
        verts = [_require_vertex(first, "first vertex")] + [
            _require_vertex(v, f"vertex {i + 2}") for i, v in enumerate(rest)
        ]
    if len(verts) < min_count:
        raise ValueError(
            f"{shape_name} needs at least {min_count} vertices, got {len(verts)}."
        )
    return verts


# ── Line ──────────────────────────────────────────────────────────────────────

class Line(_Moveable):
    """A directed line segment between two :class:`Vertex` endpoints.

    Constructors
    ------------
    Line(start, end)    – two Vertex objects
    Line(cluster)       – Cluster with exactly 2 vertices
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

    def __repr__(self) -> str:
        return f"Line({self.start} -> {self.end})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Line):
            return False
        return self.start == other.start and self.end == other.end

    def get_cluster(self) -> Cluster:
        """Return the two endpoints as a :class:`Cluster`."""
        return Cluster.from_list([self.start, self.end])

    def get_vertices(self) -> list:
        """Return ``[start, end]``. Lines are open — no closing point added."""
        return [self.start, self.end]

    # ── math ──────────────────────────────────────────────────────────────────

    def length(self) -> float:
        """Euclidean length of the segment."""
        return _side(self.start, self.end)

    def midpoint(self) -> Vertex:
        """Return a new Vertex at the exact midpoint of the segment."""
        return Vertex(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2,
        )

    def slope(self) -> float:
        """Rise-over-run slope.

        Raises
        ------
        ZeroDivisionError
            If the line is perfectly vertical (undefined slope).
        """
        dx = self.end.x - self.start.x
        if dx == 0:
            raise ZeroDivisionError("Line is vertical — slope is undefined.")
        return (self.end.y - self.start.y) / dx

    def angle(self) -> float:
        """Angle the segment makes with the positive X-axis, in degrees [0, 360)."""
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return degrees(acos(_clamp(dx / self.length(), -1.0, 1.0))) if dy >= 0 \
            else 360.0 - degrees(acos(_clamp(dx / self.length(), -1.0, 1.0)))

    def y_intercept(self) -> float:
        """Y-value where the infinite line through the segment crosses the Y-axis.

        Raises
        ------
        ZeroDivisionError
            If the line is vertical (infinite or no intercept).
        """
        return self.start.y - self.slope() * self.start.x

    def contains_point(self, v: Vertex, tol: float = 1e-9) -> bool:
        """Return True if *v* lies on the segment (within *tol*).

        Uses the collinearity test: if dist(start, v) + dist(v, end) ≈ length()
        then *v* is on the segment.

        Parameters
        ----------
        v : Vertex
            The point to test.
        tol : float
            Floating-point tolerance for the distance comparison.
        """
        _require_vertex(v, "v")
        return abs(_side(self.start, v) + _side(v, self.end) - self.length()) < tol


# ── Circle ────────────────────────────────────────────────────────────────────

class Circle:
    """Circle defined by a centre :class:`Vertex` and a radius.

    Note: Circle is not vertex-based in the same sense as the polygon shapes,
    so it does not support Cluster construction.

    Parameters
    ----------
    center : Vertex
        The centre point.
    radius : float
        The radius. Must be strictly positive.
    """

    def __init__(self, center: Vertex, radius: float):
        if not isinstance(center, Vertex):
            raise TypeError(f"center must be a Vertex, got {type(center).__name__}.")
        if radius <= 0:
            raise ValueError(f"radius must be positive, got {radius}.")
        self.center = center
        self.radius = float(radius)

    def __repr__(self) -> str:
        return f"Circle(center={self.center}, radius={self.radius})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Circle):
            return False
        return self.center == other.center and self.radius == other.radius

    def get_vertices(self, steps: int = 72) -> list:
        """Approximate the circle as *steps* evenly-spaced points (closed loop).

        Parameters
        ----------
        steps : int
            Number of points to generate (default 72 → 5° resolution).
        """
        if steps < 3:
            raise ValueError(f"steps must be at least 3, got {steps}.")
        pts = []
        for i in range(steps + 1):
            a = 2 * pi * i / steps
            pts.append((
                self.center.x + self.radius * cos(a),
                self.center.y + self.radius * sin(a),
            ))
        return pts

    # ── getters ───────────────────────────────────────────────────────────────

    def getX(self) -> float:
        """X coordinate of the centre."""
        return self.center.x

    def getY(self) -> float:
        """Y coordinate of the centre."""
        return self.center.y

    def getRadius(self) -> float:
        """The circle's radius."""
        return self.radius

    # ── math ──────────────────────────────────────────────────────────────────

    def area(self) -> float:
        """Area enclosed by the circle (π r²)."""
        return pi * self.radius ** 2

    def circ(self) -> float:
        """Circumference of the circle (2 π r)."""
        return 2 * pi * self.radius

    def diam(self) -> float:
        """Diameter of the circle (2 r)."""
        return self.radius * 2

    def arc_length(self, angle_deg: float) -> float:
        """Length of a circular arc subtended by *angle_deg* degrees.

        Parameters
        ----------
        angle_deg : float
            Central angle in degrees. Must be in (0, 360].
        """
        if not (0 < angle_deg <= 360):
            raise ValueError(f"angle_deg must be in (0, 360], got {angle_deg}.")
        return self.radius * radians(angle_deg)

    def sector_area(self, angle_deg: float) -> float:
        """Area of the pie-slice sector subtended by *angle_deg* degrees.

        Parameters
        ----------
        angle_deg : float
            Central angle in degrees. Must be in (0, 360].
        """
        if not (0 < angle_deg <= 360):
            raise ValueError(f"angle_deg must be in (0, 360], got {angle_deg}.")
        return 0.5 * self.radius ** 2 * radians(angle_deg)

    def chord_length(self, angle_deg: float) -> float:
        """Length of the chord connecting the two ends of an arc.

        Parameters
        ----------
        angle_deg : float
            Central angle in degrees subtended by the chord. Must be in (0, 360].
        """
        if not (0 < angle_deg <= 360):
            raise ValueError(f"angle_deg must be in (0, 360], got {angle_deg}.")
        return 2 * self.radius * sin(radians(angle_deg) / 2)

    def contains_point(self, vertex: Vertex) -> bool:
        """Return True if *vertex* is inside or on the boundary of the circle."""
        _require_vertex(vertex, "vertex")
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

    Vertex ordering is **counter-clockwise** by convention, though the math
    methods work regardless of winding direction.
    """

    def __init__(self, v1_or_cluster, v2: Vertex = None, v3: Vertex = None):
        super().__init__()
        verts = _cluster_or_vertices(
            v1_or_cluster,
            [v for v in (v2, v3) if v is not None],
            3,
            "Triangle",
        )
        if len(verts) != 3:
            raise ValueError(f"Triangle needs exactly 3 vertices, got {len(verts)}.")
        self.v1, self.v2, self.v3 = verts

    def __repr__(self) -> str:
        return f"Triangle({self.v1}, {self.v2}, {self.v3})"

    # ── vertex access ─────────────────────────────────────────────────────────

    def get_cluster(self) -> Cluster:
        """Return the three vertices as a :class:`Cluster`."""
        return Cluster.from_list([self.v1, self.v2, self.v3])

    def get_vertices(self) -> list:
        """Return ``[v1, v2, v3]``."""
        return [self.v1, self.v2, self.v3]

    # ── side helpers ──────────────────────────────────────────────────────────

    def side_lengths(self) -> Tuple[float, float, float]:
        """Return ``(|v1–v2|, |v2–v3|, |v3–v1|)`` — all three side lengths."""
        return (
            _side(self.v1, self.v2),
            _side(self.v2, self.v3),
            _side(self.v3, self.v1),
        )

    def getSideLength(self, va: Vertex, vb: Vertex) -> float:
        """Return the length of the side connecting two of the triangle's own vertices.

        Both *va* and *vb* must be vertices that **belong to this triangle** (i.e.
        they are the same objects as ``self.v1``, ``self.v2``, or ``self.v3``).

        Parameters
        ----------
        va : Vertex
            One endpoint — must be one of ``v1``, ``v2``, or ``v3``.
        vb : Vertex
            The other endpoint — must be one of ``v1``, ``v2``, or ``v3``.

        Returns
        -------
        float
            Euclidean distance between *va* and *vb*.

        Raises
        ------
        TypeError
            If either argument is not a Vertex.
        ValueError
            If either vertex does not belong to this triangle, or if both are
            the same vertex (a zero-length "side").

        Examples
        --------
        >>> t = Triangle(Vertex(0,0), Vertex(3,0), Vertex(0,4))
        >>> t.getSideLength(t.v1, t.v2)
        3.0
        >>> t.getSideLength(t.v1, t.v3)
        4.0
        """
        _require_vertex(va, "va")
        _require_vertex(vb, "vb")

        own = {id(self.v1), id(self.v2), id(self.v3)}
        if id(va) not in own:
            raise ValueError("va does not belong to this Triangle.")
        if id(vb) not in own:
            raise ValueError("vb does not belong to this Triangle.")
        if id(va) == id(vb):
            raise ValueError("va and vb are the same vertex — choose two different ones.")

        return _side(va, vb)

    # ── angle helpers ─────────────────────────────────────────────────────────

    @staticmethod
    def getAngle(dx1: float, dy1: float, dx2: float, dy2: float) -> float:
        """Return the angle (in degrees) between two 2-D direction vectors.

        The two vectors are given as their *x* and *y* components. This is a
        **static** method — it does not depend on any particular triangle's
        vertices, so you can call it as ``Triangle.getAngle(...)`` or as
        ``triangle_instance.getAngle(...)``.

        Parameters
        ----------
        dx1, dy1 : float
            X and Y components of the first vector (the first side's direction).
        dx2, dy2 : float
            X and Y components of the second vector (the second side's direction).

        Returns
        -------
        float
            Angle between the two vectors, in **degrees** (always in [0°, 180°]).

        Raises
        ------
        ValueError
            If either vector has zero length (direction is undefined).

        Examples
        --------
        >>> Triangle.getAngle(1, 0, 0, 1)   # X-axis vs Y-axis → 90°
        90.0
        >>> Triangle.getAngle(1, 0, 1, 0)   # same direction → 0°
        0.0
        >>> Triangle.getAngle(1, 0, -1, 0)  # opposite directions → 180°
        180.0
        """
        mag1 = sqrt(dx1 ** 2 + dy1 ** 2)
        mag2 = sqrt(dx2 ** 2 + dy2 ** 2)
        if mag1 == 0:
            raise ValueError("First vector (dx1, dy1) has zero length — angle undefined.")
        if mag2 == 0:
            raise ValueError("Second vector (dx2, dy2) has zero length — angle undefined.")
        dot = dx1 * dx2 + dy1 * dy2
        # clamp to [-1, 1] to guard against floating-point rounding outside acos domain
        return degrees(acos(_clamp(dot / (mag1 * mag2), -1.0, 1.0)))

    def angles(self) -> Tuple[float, float, float]:
        """Return the interior angles (in degrees) at each vertex.

        Returns
        -------
        tuple of float
            ``(angle_at_v1, angle_at_v2, angle_at_v3)`` — always sums to 180°
            (within floating-point tolerance).

        Uses the Law of Cosines: cos(A) = (b² + c² - a²) / (2bc), where *a*
        is the side **opposite** vertex A.
        """
        a, b, c = self.side_lengths()   # a = |v1–v2|, b = |v2–v3|, c = |v3–v1|

        # angle at v3  (opposite to side a = |v1-v2|)
        # angle at v1  (opposite to side b = |v2-v3|)
        # angle at v2  (opposite to side c = |v3-v1|)
        cos_v3 = _clamp((a ** 2 + c ** 2 - b ** 2) / (2 * a * c), -1.0, 1.0)  # wait, let me redo this properly

        # Standard labelling: side a is opposite v1, b opposite v2, c opposite v3.
        # Here: side opposite v1 = |v2–v3| = b_len, opposite v2 = |v3–v1| = c_len,
        #       opposite v3 = |v1–v2| = a_len
        a_len = _side(self.v2, self.v3)  # opposite v1
        b_len = _side(self.v3, self.v1)  # opposite v2
        c_len = _side(self.v1, self.v2)  # opposite v3

        cos_v1 = _clamp((b_len ** 2 + c_len ** 2 - a_len ** 2) / (2 * b_len * c_len), -1.0, 1.0)
        cos_v2 = _clamp((a_len ** 2 + c_len ** 2 - b_len ** 2) / (2 * a_len * c_len), -1.0, 1.0)
        cos_v3 = _clamp((a_len ** 2 + b_len ** 2 - c_len ** 2) / (2 * a_len * b_len), -1.0, 1.0)

        return (
            degrees(acos(cos_v1)),
            degrees(acos(cos_v2)),
            degrees(acos(cos_v3)),
        )

    # ── area / perimeter ──────────────────────────────────────────────────────

    def perimeter(self) -> float:
        """Sum of all three side lengths."""
        return sum(self.side_lengths())

    def area(self) -> float:
        """Area via Heron's formula: √(s(s-a)(s-b)(s-c)) where s = perimeter/2."""
        a, b, c = self.side_lengths()
        s = (a + b + c) / 2
        discriminant = s * (s - a) * (s - b) * (s - c)
        if discriminant < 0:
            # Should not happen with valid geometry; guard against float rounding
            return 0.0
        return sqrt(discriminant)

    # ── notable points ────────────────────────────────────────────────────────

    def centroid(self) -> Vertex:
        """Return the centroid (average of the three vertices) as a new Vertex.

        The centroid is the intersection of the three medians and is always
        inside the triangle.
        """
        cx = (self.v1.x + self.v2.x + self.v3.x) / 3
        cy = (self.v1.y + self.v2.y + self.v3.y) / 3
        return Vertex(cx, cy)

    # ── radii ─────────────────────────────────────────────────────────────────

    def circumradius(self) -> float:
        """Radius of the circumscribed circle (passes through all three vertices).

        Formula: R = (a · b · c) / (4 · Area)
        """
        a, b, c = self.side_lengths()
        area = self.area()
        if area == 0:
            raise ZeroDivisionError("Degenerate triangle (zero area) — circumradius undefined.")
        return (a * b * c) / (4 * area)

    def inradius(self) -> float:
        """Radius of the inscribed circle (tangent to all three sides).

        Formula: r = Area / s  where s = semi-perimeter.
        """
        perim = self.perimeter()
        if perim == 0:
            raise ZeroDivisionError("Degenerate triangle (zero perimeter) — inradius undefined.")
        return self.area() / (perim / 2)

    # ── altitudes ─────────────────────────────────────────────────────────────

    def height_from(self, v: Vertex) -> float:
        """Return the length of the altitude drawn from vertex *v* to the opposite side.

        *v* must be one of ``self.v1``, ``self.v2``, or ``self.v3``.

        Formula: h = 2 · Area / base_length

        Raises
        ------
        ValueError
            If *v* does not belong to this triangle.
        ZeroDivisionError
            If the opposite side has zero length (degenerate triangle).
        """
        _require_vertex(v, "v")
        if id(v) == id(self.v1):
            base = _side(self.v2, self.v3)
        elif id(v) == id(self.v2):
            base = _side(self.v1, self.v3)
        elif id(v) == id(self.v3):
            base = _side(self.v1, self.v2)
        else:
            raise ValueError("v does not belong to this Triangle.")
        if base == 0:
            raise ZeroDivisionError("Opposite side has zero length — altitude undefined.")
        return 2 * self.area() / base

    # ── classification ────────────────────────────────────────────────────────

    def is_equilateral(self, tol: float = 1e-9) -> bool:
        """True if all three sides are equal (within *tol*)."""
        a, b, c = self.side_lengths()
        return abs(a - b) < tol and abs(b - c) < tol

    def is_isosceles(self, tol: float = 1e-9) -> bool:
        """True if at least two sides are equal (within *tol*).

        Note: equilateral triangles are also considered isosceles.
        """
        a, b, c = self.side_lengths()
        return abs(a - b) < tol or abs(b - c) < tol or abs(a - c) < tol

    def is_scalene(self, tol: float = 1e-9) -> bool:
        """True if all three sides are different lengths (within *tol*)."""
        return not self.is_isosceles(tol)

    def is_right(self, tol: float = 1e-9) -> bool:
        """True if the largest angle is 90° (within *tol*), via Pythagoras.

        Checks a² + b² ≈ c² on the sorted side lengths.
        """
        a, b, c = sorted(self.side_lengths())
        return abs(a ** 2 + b ** 2 - c ** 2) < tol

    def is_obtuse(self, tol: float = 1e-9) -> bool:
        """True if the largest angle is greater than 90°.

        Checks a² + b² < c² on the sorted side lengths.
        """
        a, b, c = sorted(self.side_lengths())
        return (a ** 2 + b ** 2 - c ** 2) < -tol

    def is_acute(self, tol: float = 1e-9) -> bool:
        """True if all interior angles are less than 90°.

        Checks a² + b² > c² on the sorted side lengths.
        """
        a, b, c = sorted(self.side_lengths())
        return (a ** 2 + b ** 2 - c ** 2) > tol

    def __eq__(self, other):
        # Experimental new equality method that considers two triangles equal if they have the same


        if not isinstance(other, Triangle):
            return False

        def close(a, b, eps=1e-9):
            return abs(a - b) < eps

    # side lengths (order-independent)
        self_sides = sorted([
            self.getSideLength(self.v1, self.v2),
            self.getSideLength(self.v2, self.v3),
            self.getSideLength(self.v3, self.v1)
        ])

        other_sides = sorted([
            other.getSideLength(other.v1, other.v2),
            other.getSideLength(other.v2, other.v3),
            other.getSideLength(other.v3, other.v1)
        ])

        sides_equal = all(close(a, b) for a, b in zip(self_sides, other_sides))

        # angles (order-independent)
        self_angles = sorted(self.angles(self.v1, self.v2, self.v3))
        other_angles = sorted(other.angles(other.v1, other.v2, other.v3))

        angles_equal = all(close(a, b) for a, b in zip(self_angles, other_angles))

        return sides_equal or angles_equal
        
# ── Square ────────────────────────────────────────────────────────────────────

class Square(_Moveable):
    """Axis-aligned square defined by a single side length.

    Vertices are generated from the local origin ``(0, 0)``. Use the inherited
    Movement methods to position the square in the world.

    Note: Square is side-length-based, not vertex-based. Use :class:`CustomSquare`
    if you need to define corners explicitly with Vertex objects or a Cluster.

    Parameters
    ----------
    side : float
        The length of one side. Must be strictly positive.
    """

    def __init__(self, side: float):
        if side <= 0:
            raise ValueError(f"side must be positive, got {side}.")
        super().__init__()
        self.side = float(side)

    def __repr__(self) -> str:
        return f"Square(side={self.side})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Square):
            return False
        return self.side == other.side

    def get_vertices(self) -> list:
        """Return the four corners as ``(x, y)`` tuples in CCW order."""
        s = self.side
        return [(0, 0), (s, 0), (s, s), (0, s)]

    # ── math ──────────────────────────────────────────────────────────────────

    def area(self) -> float:
        """Area of the square (side²)."""
        return self.side ** 2

    def perimeter(self) -> float:
        """Perimeter of the square (4 · side)."""
        return 4 * self.side

    def diagonal(self) -> float:
        """Length of either diagonal (side · √2)."""
        return self.side * sqrt(2)

    def inscribed_radius(self) -> float:
        """Radius of the largest circle that fits inside the square (side / 2)."""
        return self.side / 2

    def circumscribed_radius(self) -> float:
        """Radius of the smallest circle that passes through all four corners (side · √2 / 2)."""
        return self.side * sqrt(2) / 2


# ── CustomSquare ──────────────────────────────────────────────────────────────

class CustomSquare(_Moveable):
    """Quadrilateral (4-sided polygon) defined by four explicit vertices.

    Unlike :class:`Square`, the vertices can be placed anywhere — supporting
    rotation, skew, and non-uniform scaling. Use this when you need full control
    over each corner.

    Constructors
    ------------
    CustomSquare(v1, v2, v3, v4)   – four Vertex objects (CCW order recommended)
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

    def __repr__(self) -> str:
        return f"CustomSquare({self.v1}, {self.v2}, {self.v3}, {self.v4})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, CustomSquare):
            return False
        return (self.v1 == other.v1 and self.v2 == other.v2 and
                self.v3 == other.v3 and self.v4 == other.v4)

    def get_cluster(self) -> Cluster:
        """Return the four vertices as a :class:`Cluster`."""
        return Cluster.from_list([self.v1, self.v2, self.v3, self.v4])

    def get_vertices(self) -> list:
        """Return ``[v1, v2, v3, v4]``."""
        return [self.v1, self.v2, self.v3, self.v4]

    # ── math ──────────────────────────────────────────────────────────────────

    def side_lengths(self) -> Tuple[float, float, float, float]:
        """Return the four consecutive side lengths as a tuple."""
        return (
            _side(self.v1, self.v2),
            _side(self.v2, self.v3),
            _side(self.v3, self.v4),
            _side(self.v4, self.v1),
        )

    def perimeter(self) -> float:
        """Sum of all four side lengths."""
        return sum(self.side_lengths())

    def area(self) -> float:
        """Area via the Shoelace (Gauss) formula. Works for any simple polygon."""
        verts = [self.v1, self.v2, self.v3, self.v4]
        n = len(verts)
        total = sum(
            verts[i].x * verts[(i + 1) % n].y - verts[(i + 1) % n].x * verts[i].y
            for i in range(n)
        )
        return abs(total) / 2

    def diagonals(self) -> Tuple[float, float]:
        """Return the lengths of the two diagonals: (|v1–v3|, |v2–v4|)."""
        return (_side(self.v1, self.v3), _side(self.v2, self.v4))


# ── SidePolygon ───────────────────────────────────────────────────────────────

class SidePolygon(_Moveable):
    """Regular *n*-sided polygon defined by a side count and side length.

    Vertices are generated around the local origin ``(0, 0)``, with the first
    point at the top. Use the inherited Movement methods to position it.

    Note: SidePolygon is parametric (side count + length). Use :class:`Mesh`
    if you need to define corners explicitly with Vertex objects or a Cluster.

    Parameters
    ----------
    sides : int
        Number of sides. Must be at least 3.
    side_length : float
        Length of each side. Must be strictly positive.
    """

    def __init__(self, sides: int, side_length: float):
        if not isinstance(sides, int) or sides < 3:
            raise ValueError(f"A polygon needs at least 3 integer sides, got {sides}.")
        if side_length <= 0:
            raise ValueError(f"side_length must be positive, got {side_length}.")
        super().__init__()
        self.sides       = sides
        self.side_length = float(side_length)

    def __repr__(self) -> str:
        return f"SidePolygon(sides={self.sides}, side_length={self.side_length})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, SidePolygon):
            return False
        return self.sides == other.sides and self.side_length == other.side_length

    def get_vertices(self) -> list:
        """Return *n* ``(x, y)`` tuples centred on the origin, first point at top."""
        r = self.side_length / (2 * sin(pi / self.sides))
        pts = []
        for i in range(self.sides):
            angle = 2 * pi * i / self.sides - pi / 2
            pts.append((r * cos(angle), r * sin(angle)))
        return pts

    # ── math ──────────────────────────────────────────────────────────────────

    def perimeter(self) -> float:
        """Total perimeter (sides · side_length)."""
        return self.sides * self.side_length

    def interior_angle(self) -> float:
        """Each interior angle in degrees: (n − 2) · 180 / n."""
        return (self.sides - 2) * 180 / self.sides

    def apothem(self) -> float:
        """Distance from the centre to the midpoint of any side (inradius).

        Formula: side_length / (2 · tan(π / n))
        """
        return self.side_length / (2 * tan(pi / self.sides))

    def area(self) -> float:
        """Area of the regular polygon: (n · side² ) / (4 · tan(π / n))."""
        return (self.sides * self.side_length ** 2) / (4 * tan(pi / self.sides))

    def circumradius(self) -> float:
        """Radius of the circumscribed circle (centre to any vertex).

        Formula: side_length / (2 · sin(π / n))
        """
        return self.side_length / (2 * sin(pi / self.sides))

    def diagonal_count(self) -> int:
        """Number of distinct diagonals: n · (n − 3) / 2."""
        return self.sides * (self.sides - 3) // 2


# ── Mesh ──────────────────────────────────────────────────────────────────────

class Mesh(_Moveable):
    """Arbitrary closed polygon from an explicit list of :class:`Vertex` objects or a Cluster.

    Constructors
    ------------
    Mesh([v1, v2, v3, ...])   – list of Vertex objects (3 or more)
    Mesh(cluster)             – a Cluster with 3 or more vertices

    Vertices are stored internally as a :class:`Cluster`. Use :meth:`get_cluster`
    to retrieve a live reference (mutations affect the Mesh).
    """

    def __init__(self, vertices):
        super().__init__()
        if isinstance(vertices, Cluster):
            cluster = vertices
        elif isinstance(vertices, list):
            if not vertices:
                raise ValueError("Mesh requires at least 3 vertices, got an empty list.")
            cluster = Cluster.from_list(vertices)
        else:
            raise TypeError(
                f"Mesh expects a list of Vertex objects or a Cluster, "
                f"got {type(vertices).__name__}."
            )
        if len(cluster) < 3:
            raise ValueError(f"Mesh needs at least 3 vertices, got {len(cluster)}.")
        self._cluster = cluster

    def __repr__(self) -> str:
        return f"Mesh({list(self._cluster.vertexes)})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Mesh):
            return False
        sv = self._cluster.vertexes
        ov = other._cluster.vertexes
        return len(sv) == len(ov) and all(a == b for a, b in zip(sv, ov))

    def get_cluster(self) -> Cluster:
        """Return the internal Cluster (live reference — mutations affect the Mesh)."""
        return self._cluster

    def get_vertices(self) -> list:
        """Return a plain list of all :class:`Vertex` objects."""
        return list(self._cluster)

    # ── math ──────────────────────────────────────────────────────────────────

    def perimeter(self) -> float:
        """Total perimeter: sum of all consecutive side lengths (closed loop)."""
        verts = self._cluster.vertexes
        n = len(verts)
        return sum(_side(verts[i], verts[(i + 1) % n]) for i in range(n))

    def area(self) -> float:
        """Area via the Shoelace (Gauss) formula. Assumes a simple (non-self-intersecting) polygon."""
        verts = self._cluster.vertexes
        n = len(verts)
        total = sum(
            verts[i].x * verts[(i + 1) % n].y - verts[(i + 1) % n].x * verts[i].y
            for i in range(n)
        )
        return abs(total) / 2

    def centroid(self) -> Vertex:
        """Return the centroid (arithmetic mean of all vertices) as a new Vertex.

        Note: this is the *vertex centroid*, not the area centroid. For
        irregular shapes they may differ; the vertex centroid is simpler
        and good enough for most rendering / game purposes.
        """
        verts = self._cluster.vertexes
        n = len(verts)
        cx = sum(v.x for v in verts) / n
        cy = sum(v.y for v in verts) / n
        return Vertex(cx, cy)
