"""
A positioner used to place a widget along the edge of its parents area

### HAnchor

---

Positions a widget at the horizontal extent of its parent node.


* **Example**

```yaml
WideGroup: !Group
    geometry: 400x20
    children:
        - !HAnchor:Text
            geometry: 50x20
            text: "I'm at the end"
```



### VAnchor

---

Positions a widget at the vertical extent of its parent node.

You may also use the alias "anchor" to reference the vachor node.


* **Example**

```yaml
TallGroup: !Group
    geometry: 40x200
    children:
        - !HAnchor:Text
            geometry: 50x20
            text: "I'm at the bottom"
```


### AAnchor

---

Positions a widget to be in the lower right corner of its parent node.


* **Example**

```yaml
BigGroup: !Group
    geometry: 400x400
    children:
        - !HAnchor:Text
            geometry: 50x20
            text: "I'm in the corner"
```
"""

from gestalt.nodes.Node import Node

class AnchorNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None, loc=None):
		super(AnchorNode, self).__init__("Anchor", name=name, layout=layout, loc=loc)
		
		self.setProperty("flow", flow, internal=True)
		self.setProperty("render-order", 1)
		
		self.subnode = subnode
		self.tocopy.append("subnode")
	
	def apply (self, generator):
		if self.name:
			self.subnode.name = self.name
			
		flow = self["flow"].val()
			
		applier = self.subnode.apply(generator)
		
		for increment in applier:
			data = yield
			
			applied_node = applier.send(data)
			applied_node.placed_order = self.placed_order
			
			if flow == "vertical":
				applied_node.position(x=applied_node["geometry"]["x"] + self["geometry"]["x"], y=int(data["__parentheight__"]) - int(applied_node["geometry"]["height"]))
			elif flow == "horizontal":
				applied_node.position(x=int(data["__parentwidth__"]) - int(applied_node["geometry"]["width"]), y=applied_node["geometry"]["y"] + self["geometry"]["y"])
			elif flow == "all":
				applied_node.position(x=int(data["__parentwidth__"]) - int(applied_node["geometry"]["width"]), y=int(data["__parentheight__"]) - int(applied_node["geometry"]["height"]))
			
			yield applied_node	
