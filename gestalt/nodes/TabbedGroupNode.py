import copy

from gestalt.Type import *
from gestalt.nodes.GroupNode import GroupNode

class TabbedGroupNode(GroupNode):
	def __init__(self, name=None, layout={}, loc=None):		
		super(TabbedGroupNode, self).__init__("TabbedGroup", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "foreground",     "$000000")
		self.setDefault(Color,  "background",     "$00000000")
		self.setDefault(Color,  "tab-color",      "$D2D2D2")
		self.setDefault(Color,  "selected",       "$A8A8A8")
		self.setDefault(Color,  "border-color",   "$000000")
		self.setDefault(String, "border-style",   "Solid")
		self.setDefault(Number, "border-width",   0)
		self.setDefault(Number, "padding",        5)
		self.setDefault(Number, "inset",          0)
		self.setDefault(Number, "offset",         0)
		self.setDefault(Number, "tabbar-height",  0, internal = True)
		self.setDefault(Font,   "font",           "-Liberation Sans - Regular - 12")
	
	def apply(self, generator):
		data = yield
		
		self.initApply(data)
		
		self.log("Generating Tabbed Group")
		output = generator.generateTabbedGroup(self, macros=data)
		
		border_size = int(output["border-width"])
		
		if output["border-color"]["alpha"] == 0:
			border_size = 0
			
		tab_bar_height = int(output["tabbar-height"])
		
		if tab_bar_height == 0:
			tab_bar_height = int(int(output["geometry"]["height"]) * 0.1)
			
		output["tabbar-height"] = Number(tab_bar_height)
		
		placed = False
		
		for childnode in self.children:
			geom = output["geometry"].val()
			
			childnode["geometry"]["width"] = int(geom["width"]) - 2 * border_size
			childnode["geometry"]["height"] = int(geom["height"]) - tab_bar_height - 2 * border_size
			
			applier = childnode.apply(generator)
			
			for increment in applier:
				child_macros = copy.copy(data)
				self.updateMacros(output, child_macros)
				
				try:
					widget = applier.send(child_macros)
						
					if widget:
						placed = True
						self.positionNext(widget)
						output.place(widget)
				except:
					break
					
		if placed:
			yield output
