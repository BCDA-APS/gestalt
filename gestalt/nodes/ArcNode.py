"""
A basic rectangle shape that can either be filled or an outline

Angles are defined in relation to the positive x axis. With 0 degrees
following that axis, and angles proceeding in the counter-clockwise
direction.

* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| background   | Color  | Widget interior color, transparent by default |
| border-color | Color  | Widget outline color, $000000 by default |
| border-width | Number | Thickness of widget outline, 2 by default |
| start-angle  | Number | Angle of the starting ray of the arc, 0 by default |
| span         | Number | Degrees that the arc covers, 90 by default |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
SimpleBox: !Arc
    geometry: 100x100
    border-width: 5
    
    start-angle: 45
    span: 180
```

"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class ArcNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ArcNode, self).__init__("Arc", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
		self.setDefault(Number, "start-angle", 0)
		self.setDefault(Number, "span", 90)
