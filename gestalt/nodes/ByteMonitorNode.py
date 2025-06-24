"""
A widget displaying the individual bits of a pv value

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| pv         | String | The PV whose bits to display |
| start-bit  | Number | The initial bit offset for the first bit being displayed, 0 by default |
| bits       | Number | The number of bits to display, increments from the start-bit, defaults to displaying till the end of the word |
| off-color  | Color  | The display color for a bit being 0, $3C643C by default |
| on-color   | Color  | The display color for a bit being 1, $00FF00 by default |
| horizontal | Bool   | Whether to arrange the display horizontally, defaults to True |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
StatusBits: !ByteMonitor
    geometry: 165x12
    
    pv: "$(P)m1.MSTA"
    bits: 15
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class ByteMonitorNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ByteMonitorNode, self).__init__("ByteMonitor", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,  "pv",          "")
		self.setDefault(Bool,    "horizontal",  True)
		self.setDefault(Number,  "start-bit",   0)
		self.setDefault(Number,  "bits",        (32 - int(self["start-bit"])))
		self.setDefault(Color,   "off-color",   "$3C643C")
		self.setDefault(Color,   "on-color",    "$00FF00")
