from .ppn import PyPen, Speed, TextAlign # added textalign in 1.3.7
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

# pydraw/__init__.py

import warnings

warnings.warn(
    "PyDraw moved to Sketchable! "
    "Please run: pip install sketchable",
    DeprecationWarning,
    stacklevel=2
)

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
    "SidePolygon",
    "Mouse",
    "Keyboard",
    "TextAlign",
    "MouseBtns"
]

# smol bugfix in v1.3.5 because not all functions were exposed as public
