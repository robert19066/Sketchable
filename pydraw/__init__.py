from .ppn import PyPen, Speed
from .sound import Speakers
from .keyboardio import Keyboard
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
    "PyPen",
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
    "SidePolygon"
]

# smol bugfix in v1.3.5 because not all functions were exposed as public
