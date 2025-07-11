"""
A widget representing a menu of other UI screens that can be opened by a user.

These other screens are detailed by the attribute `links` which is a list of
dictionaries. Within each dictionary, the following values can be defined:

* label  - The display name for the screen to open
* file   - The filepath for the screen to open
* macros - Any macros to pass the screen when opening
* replace - Optional, Whether to replace the parent screen when opening, False by default

<br>

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| links      | List   | A list of dictionaries describing the linked UI screens |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !RelatedDisplay
    foreground: *black
    background: *edit_blue

    text: "Open xxx"
    
    geometry: 10x200 x 100x20

    links:
        - { label: "File 1", file: "xxx.ui", macros: "P=1,R=A" }
```
"""

import copy
import pathlib

from gestalt.Type import *
from gestalt.nodes.Node import Node

class RelatedDisplayNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.proto_links = List(layout.pop("links", []))
		
		super(RelatedDisplayNode, self).__init__("RelatedDisplay", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,    "text",       "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Alignment, "alignment",  "Center")
		
		self.makeInternal(List, "links", [])
		
		self.tocopy.append("proto_links")

			
	def initApply(self, macros):
		copy_links = copy.deepcopy(self.proto_links)
		copy_links.apply(macros)
		
		output = []
	
		for item in copy_links:
			a_link = Dict(item)
			a_link.apply(macros)
			a_link = a_link.val()
		
			filename = a_link.get("file", "")
			
			a_link["file"] = filename.removesuffix(pathlib.PurePath(filename).suffix)
			output.append(a_link)
			
		self["links"] = List(output)
