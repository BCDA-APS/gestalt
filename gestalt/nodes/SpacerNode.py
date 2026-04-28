"""
An empty widget used to insert blank space between other elements in a layout.

Spacers produce no visible output but occupy space within flow and repeat layouts,
allowing precise control over spacing and alignment. They are commonly used to push
elements apart, create gaps, or force a minimum width or height for a container.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the dimensions of the empty space |


* **Examples**

```yaml
- !HFlow
    padding: 5
    children:
        - !Text { geometry: 100x20, text: "Left" }
        - !Spacer { geometry: 40x0 }
        - !Text { geometry: 100x20, text: "Right" }
```

A zero-dimension spacer can be used as a default placeholder in templates:

```yaml
- !Spacer
```
"""

from gestalt.nodes.Node import Node

class SpacerNode(Node):
	def __init__(self, layout=None, loc=None):
		if layout is None:
			layout = {}
		super(SpacerNode, self).__init__("Spacer", layout=layout, loc=loc)
	
	
	def apply(self, generator):
		data = yield
		
		output = generator.generateAnonymousGroup()
		output["geometry"] = self["geometry"]
		output["geometry"].apply(data)
		
		yield output
		
