"""
licenced under the MIT
This file handles shape motion, velocity, and screen-edge collision.

Changelog - V1.3:
- Motion is now a proper wrapper around any _Moveable shape.
- Added velocity, acceleration, and friction.
- Added screen-edge collision detection that checks actual transformed vertices.
- Added update() as the one-call animation tick (move → collide → refresh → sleep).
"""

from .ppn import PyPen
from .shapes import _Moveable
import time


class Motion:
    """
    Wraps any *_Moveable* shape and adds velocity-based movement plus
    screen-edge collision detection.

    How it works
    ------------
    - The shape stores its own world position (via _Moveable.move_by / move_to).
    - Motion stores a velocity vector (vx, vy) and optional friction.
    - Every call to update() does:
        1. Move the shape by the current velocity.
        2. Apply friction (slows the shape down each tick if set).
        3. Check whether any transformed vertex has crossed a screen edge.
        4. Optionally bounce (reverse the relevant velocity component).
        5. Flush the screen buffer and sleep for dt seconds.

    Quick example
    -------------
        pen = PyPen("demo")
        pen.initialise("white", 2, Speed.INSTANT, "black")

        sq = Square(60)
        sq.move_to(0, 0)

        motion = Motion(sq, pen, vx=4, vy=3)

        while True:
            pen.clear()
            pen.draw(sq, color="white", fill=True)
            motion.update()
    """

    def __init__(
        self,
        shape: _Moveable,
        pen: PyPen,
        vx: float = 0.0,
        vy: float = 0.0,
        friction: float = 1.0,
        collidable=None,
        CanExitWindow: bool = False
    ):
        if not isinstance(shape, _Moveable):
            raise TypeError(
                f"Motion requires a _Moveable shape, "
                f"got {type(shape).__name__}"
        )

        self.shape = shape
        self.pen = pen
        self.vx = float(vx)
        self.vy = float(vy)
        self.friction = float(friction)

        self.collidable = collidable or []
        self.CanExitWindow = CanExitWindow

    def _bbox(self, shape):
        verts = shape._apply_transform(shape.get_vertices())

        min_x = min(v[0] for v in verts)
        max_x = max(v[0] for v in verts)
        min_y = min(v[1] for v in verts)
        max_y = max(v[1] for v in verts)

        return min_x, max_x, min_y, max_y

    # ── velocity helpers ──────────────────────────────────────────────────────

    def set_velocity(self, vx: float, vy: float) -> "Motion":
        """Replace the current velocity vector."""
        self.vx, self.vy = float(vx), float(vy)
        return self

    def accelerate(self, ax: float, ay: float) -> "Motion":
        """Add (ax, ay) to the current velocity — useful for gravity or thrust."""
        self.vx += ax
        self.vy += ay
        return self

    def stop(self) -> "Motion":
        """Zero out velocity."""
        self.vx = self.vy = 0.0
        return self

    # ── screen bounds ─────────────────────────────────────────────────────────

    def _screen_bounds(self) -> tuple:
        """Return (left, right, bottom, top) in turtle world coordinates."""
        hw = self.pen.screen.window_width()  / 2
        hh = self.pen.screen.window_height() / 2
        return -hw, hw, -hh, hh

    # ── collision detection ───────────────────────────────────────────────────

    def check_edge_collision(self, bounce: bool = True) -> bool:
        """
        Check whether the shape's *transformed* bounding box has left the
        screen. The bounding box is built from the actual transformed vertices,
        so it respects rotation and scale.

        When *bounce* is True the relevant velocity component is reversed with
        the correct sign so the shape never tunnels through the wall.

        Returns True if at least one edge was hit.
        """
        left, right, bottom, top = self._screen_bounds()

        # Use the shape's own transform pipeline so position/rotation/scale
        # are all taken into account.
        verts = self.shape._apply_transform(self.shape.get_vertices())

        min_x = min(v[0] for v in verts)
        max_x = max(v[0] for v in verts)
        min_y = min(v[1] for v in verts)
        max_y = max(v[1] for v in verts)

        hit = False

        # Horizontal walls
        if min_x <= left:
            if bounce:
                self.vx = abs(self.vx)      # always push rightward
            hit = True
        elif max_x >= right:
            if bounce:
                self.vx = -abs(self.vx)     # always push leftward
            hit = True

        # Vertical walls
        if min_y <= bottom:
            if bounce:
                self.vy = abs(self.vy)      # always push upward
            hit = True
        elif max_y >= top:
            if bounce:
                self.vy = -abs(self.vy)     # always push downward
            hit = True

        return hit
    
    def check_shape_collision(self):
        my_minx, my_maxx, my_miny, my_maxy = self._bbox(self.shape)

        for obj in self.collidable:

            other_minx, other_maxx, other_miny, other_maxy = (
                self._bbox(obj)
            )

            overlap = (
                my_maxx >= other_minx and
                my_minx <= other_maxx and
                my_maxy >= other_miny and
                my_miny <= other_maxy
            )

            if overlap:

                # basic bounce
                self.vx *= -1
                self.vy *= -1

                return obj

        return None

    def is_on_screen(self) -> bool:
        """Return True when the shape's bounding box is fully inside the screen."""
        left, right, bottom, top = self._screen_bounds()
        verts = self.shape._apply_transform(self.shape.get_vertices())
        return (
            all(v[0] >= left  for v in verts) and
            all(v[0] <= right for v in verts) and
            all(v[1] >= bottom for v in verts) and
            all(v[1] <= top    for v in verts)
        )

    # ── main tick ─────────────────────────────────────────────────────────────

    def update(
        self,
        dt: float = 0.016,
        bounce: bool = True
    ):

        self.shape.move_by(self.vx, self.vy)

        self.vx *= self.friction
        self.vy *= self.friction

        if not self.CanExitWindow:
            self.check_edge_collision(
                bounce=bounce
            )

        self.check_shape_collision()

        self.pen.screen.update()

        time.sleep(dt)

        return self

    # ── dunder ────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"Motion(shape={self.shape!r}, "
            f"vx={self.vx}, vy={self.vy}, friction={self.friction})"
        )