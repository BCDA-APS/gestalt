"""
A basic rectangle shape that can either be filled or an outline

* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| background   | Color  | Widget interior color, transparent by default |
| border-color | Color  | Widget outline color, $000000 by default |
| border-width | Number | Thickness of widget outline, 2 by default |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
SimpleBox: !Rectangle
    geometry: 100x100
    border-width: 5
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class RectangleNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(RectangleNode, self).__init__("Rectangle", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
