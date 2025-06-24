"""
A widget representing a button that writes a value to a pv when pressed

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| pv         | String | The PV that will be written to |
| value      | String | The value to write to the PV |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !MessageButton
    foreground: *black
    background: *edit_blue

    text: "Write Value"
    
    geometry: 10x200 x 100x20
    
    pv: "xxx:yyy:zzz"
    value: 1
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class MessageButtonNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(MessageButtonNode, self).__init__("MessageButton", name=name, layout=layout, loc=loc)
		self.setDefault(String,    "text",       "")
		self.setDefault(String,    "pv",         "")
		self.setDefault(String,    "value",      "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Alignment, "alignment",  "Center")
