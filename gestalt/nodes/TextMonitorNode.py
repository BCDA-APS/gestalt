"""
A widget representing a text display field

* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| foreground   | Color     | Widget foreground color |
| background   | Color     | Widget background color |
| border-color | Color     | Widget border color |
| border-width | Number    | Widget border thickness in pixels |
| font         | Font      | Widget display font |
| alignment    | Alignment | Display text alignment |
| format       | String    | Text display format, value is one of "String, Decimal, Engineering, Exponential, Compact, Hexadecimal, Binary" |
| pv           | String    | The PV to read data from |
| visibility   | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !TextMonitor
    geometry: 5x0 x 120x20
    
    pv: "$(P)$(R)Description_RBV"
    
    alignment: CenterRight
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class TextMonitorNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(TextMonitorNode, self).__init__("TextMonitor", name=name, layout=layout, loc=loc)
	
		self.setDefault(String,    "pv",           "")
		self.setDefault(Color,     "foreground",   "$000000")
		self.setDefault(Color,     "background",   "$00000000")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(String,    "border-style", "Solid")
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(String,    "format",       "Decimal")
		self.setDefault(Alignment, "alignment",    "CenterLeft")
