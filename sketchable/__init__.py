from .ppn import Sketcher, Speed, TextAlign # added textalign in 1.3.7
from .sound import Speakers
from .externals import Mouse, Keyboard, MouseBtns # remade in 1.3.7
from .shapes import (
    Circle,
    Triangle,
    Vertex,
    CustomSquare,
    Line,
    Mesh,
    Square,
    Cluster,
    SidePolygon
)
from .motion import Motion


__all__ = [
    "Sketcher",
    "Circle",
    "Vertex",
    "CustomSquare",
    "Line",
    "Square",
    "Speed",
    "Motion",
    "Speakers",
    "Keyboard",
    "Triangle",
    "Mesh",
    "Cluster",
    "SidePolygon",
    "Mouse",
    "Keyboard",
    "TextAlign",
    "MouseBtns"
]

# smol bugfix in v1.3.5 because not all functions were exposed as public
