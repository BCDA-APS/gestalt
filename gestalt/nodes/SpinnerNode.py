"""
A widget that provides a numeric input control with increment and decrement buttons.

On caQtDM, this renders as a wheel switch (caNumeric) with digit-by-digit up/down arrows.
On Phoebus, this renders as a Spinner with increment/decrement buttons.
On PyDM, this renders as a PyDMSpinbox with standard up/down controls.


* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| pv           | String    | The PV to read from and write to |
| foreground   | Color     | Widget foreground color |
| background   | Color     | Widget background color |
| precision    | Number    | Number of decimal places, -1 by default (uses PV precision) |
| font         | Font      | Widget display font |
| minimum      | Number    | Minimum allowed value, uses PV limits by default |
| maximum      | Number    | Maximum allowed value, uses PV limits by default |
| enabled      | Bool      | Whether the widget is interactive, True by default |
| alarm-border | Bool      | Change border color based on PV alarm severity, False by default |
| visibility   | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Examples**

```yaml
SetpointControl: !Spinner
    geometry: 120x30
    pv: "$(P)$(R)Setpoint"
    precision: 2
```

With explicit limits:

```yaml
TemperatureEntry: !Spinner
    geometry: 120x30
    pv: "$(P)$(R)Temperature"
    precision: 1
    minimum: 0
    maximum: 100
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class SpinnerNode(Node):
	def __init__(self, name=None, layout=None, loc=None):
		if layout is None:
			layout = {}
		super(SpinnerNode, self).__init__("Spinner", name=name, layout=layout, loc=loc)

		self.setDefault(String, "pv",         "")
		self.setDefault(Color,  "foreground", "$000000")
		self.setDefault(Color,  "background", "$57CAE4")
		self.setDefault(Font,   "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Number, "precision",  -1)
		self.setDefault(Number, "minimum",    -1)
		self.setDefault(Number, "maximum",    -1)
		self.setDefault(Bool,   "enabled",    True)
		self.setDefault(Bool,   "alarm-border", False)
