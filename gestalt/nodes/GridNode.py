"""
Iterates over a given macro in the input file named by the attribute `repeat-over`, generating 
a copy of all children widgets as a group. Configures each such group according to the input 
macros and then positions the set of widgets in a grid pattern. The group's starting X and Y 
positions are set such that each group is a number of pixels away from the edges of any other 
group according to the value of the attribute `padding`. 

If the macro named by `repeat-over` is parsed and found to be a number, then the node will iterate
a number of times specified by the macro. On each loop, the children widgets will be provided with
the macros `N`, `__index__`, `__col__`, and `__row__` to use to configure themselves. `__index__` 
is a number that starts at zero and increments by one every iteration of the loop. `N` is similar, 
but starts at a value specified by the attribute `start-at`. `__row__` and `__col__` specify the
current 0-indexed position within the grid where the group will be generated.

If, instead, `repeat-over` names a macro that is found to be a list of dictionaries, then the
dictionaries will be treated as the macros to use to configure the children widgets. The loop
will iterate over each of the specified mappings and will provide the children elements of the
group with those macros (alongside any other macros in the data file). All the same macros
mentioned above will also be included.

The number of columns and rows in the node's grid pattern are determined by the number of iterations
specified by `repeat-over` combined with the attribute `aspect-ratio`. Defaulting to 1.0, `aspect-ratio` 
is the ratio between the number of columns to the number of rows to use. So an `aspect-ratio` of 2.0
would be specifying that the node should attempt to have twice as many columns as rows. This is
an idealized ratio and it may not be possible to exactly match the ratio as given with the number of
elements a user provides.

You can also control the shape by specifying the minimum and maximum numbers of columns and rows. Using
'min-cols', 'max-cols', 'min-rows', and 'max-rows', you can restrict the automatic shaping done based
off of 'aspect-ratio'. If there is a conflict between the number of iterations, the aspect-ratio, and
the minimum/maximum values, then the 'horizontal' attribute will be used to determine which restrictions
to weight heavier. If 'horizontal' is True, then size will break any horizontal constraints (adding additional
columns). If 'horizontal' is False, then the vertical constraints will be broken (adding additional rows).


* **Special Attributes**

|       Name     |  Type  | Description|
|----------------|--------|------------|
| children       | List   | A list of widgets to use as a template to copy in a grid pattern |
| repeat-over    | String | The name of a macro that will be provided within the input data file |
| variable       | String | The name under which to provide the value of the loop index, 'N' by default |
| start-at       | Number | An offset value to the loop index to provide children widgets |
| padding        | Number | The number of pixels between each widget group |
| aspect-ratio   | Double | A ratio indicating the relative number of columns to the number of rows in the grid |
| background     | Color  | A fill color behind the entirety of each template copy |
| border-color   | Color  | The color of the group's border surrounding each template copy |
| border-width   | Number | The thickness of the group's border in pixels |
| reverse        | Bool   | Iterate over repeat-over in a reversed order |
| horizontal     | Bool   | Fill direction of the layout. Macros will be mapped to widgets across columns first, then proceed to the next row, rather than the reverse. True by default |
| visibility     | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |
| ignore-empty   | Bool   | Defines whether or not to adjust positioning of elements if a repeated instance is an empty group. Useful for dealing with Conditional nodes. default: False |


* **Example**

```yaml
LED_Grid: !Grid
    geometry: 160x170 x 0x0
    aspect-ratio: 1.5
    repeat-over: "LEDs"
    
    padding: 10

    children:
        - !LED
            <<: *alarm_led
            geometry: 20x20
```
"""

import math

from gestalt.Type import *
from gestalt.nodes.LayoutNode import LayoutNode

class GridNode(LayoutNode):
	def __init__(self, name=None, layout={}, loc=None):
		super(GridNode, self).__init__(name=name, layout=layout, loc=loc)
	
		self.makeInternal(Number, "min-rows", 0)
		self.makeInternal(Number, "min-cols", 0)
		self.makeInternal(Number, "max-rows", 0)
		self.makeInternal(Number, "max-cols", 0)
		
		self.makeInternal(Number, "padding-x", self["padding"])
		self.makeInternal(Number, "padding-y", self["padding"])
		
		self.makeInternal(Double, "aspect-ratio", 1.0)
		self.makeInternal(Bool,   "horizontal", True)
		
		self.makeInternal(Number, "index-x", 0)
		self.makeInternal(Number, "index-y", 0)
		
	def initApply (self, data):
		self["index-x"] = 0
		self["index-y"] = 0
		self["aspect-ratio"].apply(data)
				
		super().initApply(data)
		
	def updateMacros(self, output, macros):
		super().updateMacros(output, macros)
		
		macros.update({
			"__col__" : self["index-x"].val(),
			"__row__" : self["index-y"].val()})

	def positionNext(self, line):
		ratio = self["aspect-ratio"].val()
		
		cols_calc = round(math.sqrt(int(self["num-items"]) * float(ratio)))
		rows_calc = round(math.sqrt(int(self["num-items"]) / float(ratio)))
		
		rows = rows_calc
		cols = cols_calc
			
		rows = max(rows, int(self["min-rows"]))
		cols = max(cols, int(self["min-cols"]))
		
		while cols * rows < int(self["num-items"]):
			if self["horizontal"]:
				cols += 1
			else:
				rows += 1
		
		if int(self["max-rows"]) > 0: 
			rows = min(rows, int(self["max-rows"]))
		if int(self["max-cols"]) > 0:
			cols = min(cols, int(self["max-cols"]))
		
		cols_diff = (cols != cols_calc)
		rows_diff = (rows != rows_calc)
		
		if cols_diff and (not rows_diff or self["horizontal"]):
			rows = math.ceil(int(self["num-items"]) / float(cols))
		elif rows_diff and (not cols_diff or not self["horizontal"]):
			cols = math.ceil(int(self["num-items"]) / float(rows))
			
		pos_x = int(self["index-x"]) * (line["geometry"]["width"] + int(self["padding-x"]))
		pos_y = int(self["index-y"]) * (line["geometry"]["height"] + int(self["padding-y"]))
		
		line.position(x=pos_x, y=pos_y)

		span, scale = "index-x", "index-y"
		
		if self["horizontal"]:
			self["index-x"] = self["index-x"].val() + 1
			
			if int(self["index-x"]) >= cols:
				self["index-x"] = 0
				self["index-y"] = self["index-y"].val() + 1
				
		else:
			self["index-y"] = self["index-y"].val() + 1
			
			if int(self["index-y"]) >= rows:
				self["index-y"] = 0
				self["index-x"] = self["index-x"].val() + 1
				
