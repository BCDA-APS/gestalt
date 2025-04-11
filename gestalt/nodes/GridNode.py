import math

from gestalt.Type import *
from gestalt.nodes.LayoutNode import LayoutNode

class GridNode(LayoutNode):
	def __init__(self, name=None, layout={}, loc=None):
		super(GridNode, self).__init__(name=name, layout=layout, loc=loc)
	
		self.makeInternal(Number, "max-rows", -1)
		self.makeInternal(Number, "max-cols", -1)
		
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
		
		cols = round(math.sqrt(int(self["num-items"]) * float(ratio)))
		rows = round(math.sqrt(int(self["num-items"]) / float(ratio)))
		
		if int(self["max-rows"]) > 0 and int(self["max-rows"]) <= rows:
			rows = int(self["max-rows"])
			cols = math.ceil(int(self["num-items"]) / float(rows))
			
		if int(self["max-cols"]) > 0 and int(self["max-cols"]) <= cols:
			cols = int(self["max-cols"])
			rows = math.ceil(int(self["num-items"]) / float(cols))
		
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
