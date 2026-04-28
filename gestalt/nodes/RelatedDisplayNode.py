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


* **Examples**

```yaml
- !RelatedDisplay
    geometry: 120x30
    background: *menu_green
    foreground: *white
    text: "Motor Details"

    links:
        - { label: "Help",  file: "motorx_help",  macros: "P=$(P),M=$(M)" }
        - { label: "More",  file: "motorx_more",  macros: "P=$(P),M=$(M)" }
        - { label: "Setup", file: "motorx_setup", macros: "P=$(P),M=$(M)" }
        - { label: "All",   file: "motorx_all",   macros: "P=$(P),M=$(M)" }
```

The file extension is automatically appended based on the output format.
The `replace` option can be used to open the display in the same window:

```yaml
- !RelatedDisplay
    geometry: 100x20
    text: "Open"
    links:
        - { label: "Main", file: "main_screen", macros: "P=$(P)", replace: true }
```
"""

import copy
import pathlib

from gestalt.Type import *
from gestalt.nodes.Node import Node

class RelatedDisplayNode(Node):
	def __init__(self, name=None, layout=None, loc=None):
		if layout is None:
			layout = {}
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
