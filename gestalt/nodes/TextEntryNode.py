"""
A widget representing a text entry field.

* **Special Attributes**

|    Name    |    Type   | Description|
|------------|-----------|------------|
| geometry   | Rect      | A rectangle describing the position and dimensions of the widget |
| foreground | Color     | Widget foreground color |
| background | Color     | Widget background color |
| font       | Font      | Widget display font |
| alignment  | Alignment | Display text alignment |
| format     | String    | Text display format, value is one of "String, Decimal, Engineering, Exponential, Compact, Hexadecimal, Binary" |
| pv         | String    | The PV that will be written to |
| visibility | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Examples**

```yaml
- !TextEntry
    geometry: 5x0 x 120x20
    pv: "$(P)$(R)Description"
    alignment: BottomLeft
```

Entry fields are typically styled with a distinct background color to indicate they are editable:

```yaml
- !TextEntry
    geometry: 120x20
    background: *edit_blue
    format: "String"
    pv: "$(P)$(R)UserName"
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class TextEntryNode(Node):
	def __init__(self, name=None, layout=None, loc=None):
		if layout is None:
			layout = {}
		super(TextEntryNode, self).__init__("TextEntry", name=name, layout=layout, loc=loc)
	
		self.setDefault(String,    "pv",         "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(String,    "format",     "String")
		self.setDefault(Alignment, "alignment",  "CenterLeft")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Color,     "foreground", "$000000")
