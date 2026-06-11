"""
A widget that uses a slider to control output to a pv

* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| horizontal   | Bool      | Whether to arrange the display horizontally, defaults to True |
| minimum      | Number    | Minimum allowed value, uses PV limits by default |
| maximum      | Number    | Maximum allowed value, uses PV limits by default |
| enabled      | Bool      | Whether the widget is interactive, True by default |
| alarm-border | Bool      | Change border color based on PV alarm severity, False by default |
| pv           | String    | The PV being monitored |
| visibility   | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !Slider
    geometry: 140x0 x 120x20
    pv: "$(P)Ao10"
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class SliderNode(Node):
	def __init__(self, name=None, layout=None, loc=None):
		if layout is None:
			layout = {}
		super(SliderNode, self).__init__("Slider", name=name, layout=layout, loc=loc)
		
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(String, "pv",         "")
		self.setDefault(Number, "minimum",    -1)
		self.setDefault(Number, "maximum",    -1)
		self.setDefault(Bool,   "enabled",    True)
		self.setDefault(Bool,   "alarm-border", False)
		

