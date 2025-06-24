"""
A positioner used to stretch a widget to fill the space provided by its parent widget

### AStrech

---

Determines a widget's width and height to match up respectively with the widget's parent values.

* **Example**

```yaml
Fill_Parent: !astretch:Text            
    text: "Middle"
    alignment: CenterLeft
```



### HStretch

---

Determines a widget's width to match up with the size of the widget's parent width.


* **Example**

```yaml
UITitle: !hstretch:Text
    geometry: 0x32
            
    text: "Middle"
    alignment: CenterLeft
```



### VStretch

---

Determines a widget's width to match up with the size of the widget's parent width.

You may also use the alias "stretch" to reference the vstretch node.


* **Example**

```yaml
UITitle: !vstretch:Text
    geometry: 32x0
            
    text: "Middle"
    alignment: CenterLeft
```
"""

import copy

from gestalt.nodes.Node import Node

class StretchNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None, loc=None):
		super(StretchNode, self).__init__("Stretch", name=name, layout=layout, loc=loc)
				
		self.setProperty("flow", flow, internal=True)
		self.setProperty("render-order", 1)
		
		self.subnode = subnode
		self.tocopy.append("subnode")
		
	
	def apply (self, generator):
		the_node = copy.deepcopy(self.subnode)
		
		if self.name:
			the_node.name = self.name
		
		applier = the_node.apply(generator)
		
		for increment in applier:
			data = yield
			
			flow = self["flow"].val()
			
			if flow == "vertical" or flow == "all":
				the_node["geometry"]["height"] = data["__parentheight__"]
			if flow == "horizontal" or flow=="all":
				the_node["geometry"]["width"] = data["__parentwidth__"]
			
			applied_node = applier.send(data)
			applied_node.placed_order = self.placed_order
			
			yield applied_node
