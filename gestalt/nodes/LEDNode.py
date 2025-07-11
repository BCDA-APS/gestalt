"""
A widget that changes color based upon the value of a given pv. Has one of three states,
true, false, or undefined based upon a match with values given by the widget.


* **Special Attributes**

|       Name      |    Type   | Description|
|-----------------|-----------|------------|
| geometry        | Rect      | A rectangle describing the position and dimensions of the widget |
| square          | Bool      | Change widget shape to rectangular rather than circular |
| false-value     | Number    | Set widget to false-color when pv value equals false-value, 0 by default |
| true-value      | Number    | Set widget to true-color when pv value equals true-value, 1 by default |
| false-color     | Color     | The display color for a false value, $3C643C by default |
| true-color      | Color     | The display color for a true value, $00FF00 by default |
| undefined-color | Color     | The display color for any other value, $A0A0A4 by default |
| border-color    | Color     | Widget border color, $000000 by default |
| pv              | String    | The PV to read data from |
| visibility      | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
OnOff_Readback: !LED
    pv: "$(P)userCalcEnable.VAL"
    
    geometry: 24x24
    square: true
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class LEDNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(LEDNode, self).__init__("LED", name=name, layout=layout, loc=loc)
	
		self.setDefault(String, "pv",             "")
		self.setDefault(Bool,   "square",         False)
	
		self.setDefault(Color, "false-color",     "$3C643C")
		self.setDefault(Color, "true-color",      "$00FF00")
		self.setDefault(Color, "undefined-color", "$A0A0A4")
		self.setDefault(Color, "border-color",    "$000000")
	
		self.setDefault(Number, "false-value", 0)
		self.setDefault(Number, "true-value", 1)
