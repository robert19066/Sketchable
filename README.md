<p align="center"> <a href="https://postimg.cc/Pp2zGxwG"> <img src="https://i.postimg.cc/wMdWmRxB/caspdlowekk.png" alt="image" /> </a> </p>


<h1 align="center">Documentation for the PyDraw 2D Graphical Engine</h1>
The PyDraw system constitutes a high-level abstraction layer and computational framework developed upon the Python turtle module. This software architecture facilitates the execution of two-dimensional graphical rendering, kinematic simulations, and geometric analysis by mitigating the complexities associated with low-level buffer management and coordinate system synchronization.

The software is distributed under the terms of the GNU Affero General Public License version 3.0 (AGPL3).

## **I. Technical Capabilities**

* **Execution Environment:** The framework transforms the native procedural drawing interface into a persistent execution state suitable for iterative simulation loops. The "PyMaze" implementation serves as a primary demonstration of grid-based pathfinding and real-time state updates.  
* **Geometric Primitives:** The system provides an extensive library of geometric entities, each possessing internal methods for the calculation of surface area, perimeter, and topological verification.  
* **Coordinate Transformations:** All entities inherit from a foundational transformation class, enabling precise translation, rotation, and scaling within a Cartesian coordinate system.  
* **Kinematic Modeling:** The motion subsystem integrates velocity vectors, gravitational acceleration, and frictional coefficients. Automated boundary detection ensures the containment of entities within the defined viewport through the application of reflective collision logic.  
* **Rendering Pipeline:** The PyPen component provides a unified interface for the rasterization of all supported geometric structures via a centralized rendering method.

## **II. Specification of Geometric Entities**

The instantiation of geometric primitives within the PyDraw environment requires adherence to the following structural definitions. Every entity inherits transformation capabilities from the \_Moveable superclass.

from shapes import Vertex, Line, Circle, Triangle, Square, VertexSquare, Ellipse, RegularPolygon, Polygon

\# 1\. Vertex (A fundamental coordinate point within the 2D manifold)  
`v1 = Vertex(0, 0\)  `
`v2 = Vertex(100, 100\)`

\# 2\. Line (A linear segment established between two vertices)  
`entity\_line = Line(start=v1, end=v2)`

\# 3\. Circle (Defined by a central vertex and a scalar radius)  
`entity\_circle = Circle(center=v1, radius=45.5)`

\# 4\. Triangle (A three-sided polygon defined by three vertices)  
`triangle = Triangle(v1, v2, Vertex(-50, 50))`

\# 5\. Square (A regular quadrilateral instantiated at the origin)  
`square = Square(side=60).move_to(10, 10)`

\# 6\. VertexSquare (A quadrilateral defined by four distinct vertices)  
`square = VertexSquare(v1, v2, Vertex(50, -50), Vertex(-50, 50))`

\# 7\. Ellipse (Defined by a center and two semi-axes, 'a' and 'b')  
`ellipse = Ellipse(center=v1, a=80, b=40)`

\# 8\. Regular Polygons (Equilateral and equiangular n-gons)  
`hexagon = RegularPolygon(sides=6, side_length=30)`

\# 9\. Custom Polygon (An arbitrary n-gon defined by an ordered list of vertices)  
`custom_poly = Polygon([Vertex(0,0), Vertex(50, 20), Vertex(30, 80)])`

## **III. Kinematic and Motion Subsystems**

The Motion class provides a wrapper for the integration of physical properties into geometric entities. This class manages the transition from static rendering to dynamic simulation by overseeing velocity components and environmental constraints.

### **Implementation Protocol:**

1. **Entity Selection:** A geometric entity must be initialized.  
2. **Kinematic Wrapping:** A Motion instance is constructed, incorporating the target entity, the rendering interface, initial velocity components (vx, vy), and the coefficient of friction.  
3. **State Iteration:** The update() method must be executed within the primary simulation loop.

### **Kinematic Simulation Example:**

from pypen import PyPen, Speed  
from shapes import RegularPolygon  
from motion import Motion

\# Initialization of the rendering interface  
engine \= PyPen("Kinematic Simulation Environment")  
engine.initialise(PenColor="cyan", size=3, speed=Speed.INSTANT, BackgroundColor="black")

\# Instantiation of a regular hexagon  
hex\_shape \= RegularPolygon(sides=6, side\_length=40)  
hex\_shape.move\_to(0, 0\)

\# Construction of the kinematic wrapper  
\# Friction is defined as a scalar multiplier where 1.0 represents an absence of kinetic energy loss.  
physics_body = Motion(  
    shape=hex_shape,   
    pen=engine,   
    vx=8.5,   
    vy=6.0,   
    friction=1.0   
)

\# Application of constant acceleration (e.g., simulated gravitational forces)  
physics_body.accelerate(ax=0, ay=-0.5)

\# Primary simulation loop  
while True:  
    engine.clear()                                  
    engine.draw(hex_shape, color="cyan")            


## **IV. Comprehensive Demonstration: PyMaze**

A full realization of the engine's capabilities is documented in the test.py module. The "PyMaze" application demonstrates the integration of user-input handling, grid-based collision logic, and real-time head-up display (HUD) rendering. The showcase uses turtle and PyDraw

## **V. Scholarly Attributions and Development Context**

The PyDraw framework was conceptualized and implemented to resolve the lack of standardized geometric abstraction in contemporary educational graphics libraries. It is noteworthy that the project was initiated and brought to fruition by an individual at the secondary education level.

While certain algorithmic complexities, such as the Shoelace formula for area calculation, were refined through the utilization of computational linguistics tools, the overarching software architecture, kinematic logic, and design patterns are the result of original scholarly inquiry.
