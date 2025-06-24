"""
A widget representing a menu that gets its options from an enumerable pv


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| pv         | String | The PV containing the enumerable value |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !Menu
    foreground: *black
    background: *edit_blue
    geometry: 355x0 x 80x20
    pv: $(P){Instance}:EnableCallbacks
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class MenuNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(MenuNode, self).__init__("Menu", name=name, layout=layout, loc=loc)
	
		self.setDefault(String, "pv", "")
		self.setDefault(Color, "background", "$57CAE4")
		self.setDefault(Color, "foreground", "$000000")
