"""
A widget that references and embeds another UI file


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| file       | String | The filepath of the file to display |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
EmbededDisplay: !Include
    file: "another_file"  # Can leave off file extension, will be appended with correct filetype for the output UI tool
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

import pathlib

class IncludeNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(IncludeNode, self).__init__("Include", name=name, layout=layout, loc=loc)
		
		self.setDefault(String, "file", "")
		self.setDefault(String, "macros", "")

	def initApply(self, macros):
		filename = str(self["file"])
		
		self["file"] = filename.removesuffix(pathlib.PurePath(filename).suffix)
