"""
A container widget that holds children elements within a bordered, optionally filled area.

Groups serve as the basic building block for organizing widgets. Children are
positioned relative to the group's origin, offset by the group's margins and
border width. The group automatically grows to fit its children.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| children     | List   | A list of child widgets contained by this group |
| background   | Color  | A fill color for the group, defaults to transparent |
| border-color | Color  | The color of the group's border, defaults to $000000 |
| border-width | Number | The thickness of the group's border in pixels, defaults to 0 |
| margins      | Rect   | Inset spacing within the group's border, defaults to 0x0x0x0 |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
StatusBox: !Group
    geometry: 200x100
    background: $EEEEEE
    border-width: 2
    border-color: *black
    margins: 5x5x5x5
    
    children:
        - !Text
            geometry: 0x0 x 190x20
            text: "Device Status"
            alignment: Center
            
        - !TextMonitor
            geometry: 0x25 x 190x20
            pv: "$(P)$(R)Status_RBV"
```

Groups can also be used as visibility containers, showing or hiding
their children based on a PV value:

```yaml
ConditionalControls: !Group
    visibility: "$(P)$(R)Enabled"
    children:
        - !MessageButton
            geometry: 100x30
            text: "Start"
            pv: "$(P)$(R)Start"
            value: 1
```
"""

import copy

from gestalt.Type import *
from gestalt.nodes.Node import Node

class GroupNode(Node):
	def __init__(self, classname="Group", name=None, node=None, layout=None, loc=None, anonymous=False):
		if layout is None:
			layout = {}
		super(GroupNode, self).__init__(classname, name=name, node=node, layout=layout, loc=loc)

		self.children = []

		if not node:
			initial = self.pop("children", [])

			if isinstance(initial, dict):
				for childname, child in initial.items():
					child.name = childname
					self.append(child)

			elif isinstance(initial, list):
				for child in initial:
					self.append(child)

			self.makeInternal(Rect, "margins", "0x0x0x0")

		self.setDefault(Color, "background", "$00000000")
		self.setDefault(Rect, "margins", "0x0x0x0", internal=True)
		self.setDefault(Bool, "ignore-empty", False, internal=True)
		self.setDefault(Number, "border-width",   0)
		self.makeInternal(Bool, "anonymous", anonymous)


	def append(self, child, keep_original=False):
		self.log("Adding child node " + child.__repr__())

		to_append = child

		if not keep_original:
			to_append = copy.deepcopy(child)

		if not to_append.placed_order:
			to_append.placed_order = len(self.children)

		self.children.append(to_append)

	def __iter__(self):
		return sorted(self.children, key=lambda x: int(x["render-order"])).__iter__()

	def write_order(self):
		return sorted(self.children, key=lambda x: (int(x["z-order"]), int(x.placed_order or 0))).__iter__()


	def place(self, child, x=None, y=None, keep_original=False):
		if (child == None):
			return

		self.append(child, keep_original=keep_original)

		child_node = self.children[-1]

		margins = self["margins"].val()

		child_geom = child_node["geometry"].val()
		my_geom = self["geometry"].val()
		border = int(self["border-width"])

		if x is not None:
			child_node["geometry"]["x"] = int(x) + int(margins["x"]) + border
		else:
			child_node["geometry"]["x"] = int(child_geom["x"]) + int(margins["x"]) + border

		if y is not None:
			child_node["geometry"]["y"] = int(y) + int(margins["y"]) + border
		else:
			child_node["geometry"]["y"] = int(child_geom["y"]) + int(margins["y"]) + border

		# Don't use child_geom for x/y as the value may have updated
		right_edge  = int(child_node["geometry"]["x"]) + int(child_geom["width"]) + int(margins["width"])
		bottom_edge = int(child_node["geometry"]["y"]) + int(child_geom["height"]) + int(margins["height"])

		if right_edge > int(my_geom["width"]):
			self.log("Resizing width to " + str(right_edge))
			self["geometry"]["width"] = right_edge

		if bottom_edge > int(my_geom["height"]):
			self.log("Resizing height to " + str(bottom_edge))
			self["geometry"]["height"] = bottom_edge

	def positionNext(self, child):
		pass

	def updateMacros(self, output, macros):
		geom = output["geometry"].val()
		margins = output["margins"].val()
		border = int(output["border-width"])

		macros.update({
			"__parentx__" : int(geom["x"]),
			"__parenty__" : int(geom["y"]),
			"__parentwidth__" : int(geom["width"]) - int(margins["x"]) - int(margins["width"]) - 2 * border,
			"__parentheight__" : int(geom["height"]) - int(margins["y"]) - int(margins["height"]) - 2 * border,
			"__parentcenterx__" : int((int(geom["width"]) - int(margins["x"]) - int(margins["width"]) - 2 * border) / 2 + int(margins["x"]) + border),
			"__parentcentery__" : int((int(geom["height"]) - int(margins["y"]) - int(margins["height"]) - 2 * border) / 2 + int(margins["y"]) + border)})


	def apply (self, generator):
		data = yield

		self.initApply(data)

		self.log("Generating group node")
		output = generator.generateGroup(self, macros=data)

		basically_anonymous = (int(output["border-width"]) == 0 or int(output["border-color"].val()["alpha"]) == 0) and int(output["background"].val()["alpha"]) == 0 and ("visibility" not in output) and self.classname != "TabNode"

		if output["anonymous"] or basically_anonymous:
			temp = generator.generateAnonymousGroup()
			temp["geometry"] = output["geometry"]
			temp["margins"] = output["margins"]
			temp["ignore-empty"] = output["ignore-empty"]
			output = temp

		placed = False

		for child in self:
			applier = child.apply(generator)

			for increment in applier:
				child_macros = copy.copy(data)

				self.updateMacros(output, child_macros)

				# Center Node wants to stop iteration in send, so we need try/except
				try:
					widget = applier.send(child_macros)

					if widget:
						placed = True
						widget.placed_order = child.placed_order
						self.positionNext(widget)
						output.place(widget)
				except RuntimeError as e:
					if str(e) == "generator raised StopIteration":
						break
					else:
						raise e
				except StopIteration:
					break

		if not output["ignore-empty"] or placed:
			yield output

	def __deepcopy__(self, memo):
		output = super().__deepcopy__(memo)

		output.children = copy.copy(self.children)

		return output
