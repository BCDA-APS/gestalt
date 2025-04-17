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
		
		cols = round(math.sqrt(int(self["num-items"]) * float(ratio)))
		rows = round(math.sqrt(int(self["num-items"]) / float(ratio)))
		
		if int(self["max-rows"]) > 0: 
			rows = min(rows, int(self["max-rows"]))
		if int(self["max-cols"]) > 0:
			cols = min(cols, int(self["max-cols"]))
			
		rows = max(rows, int(self["min-rows"]))
		cols = max(cols, int(self["min-cols"]))
		
		while cols * rows < int(self["num-items"]):
			if self["horizontal"]:
				cols += 1
			else:
				rows += 1
		
		if self["horizontal"]:
			rows = math.ceil(int(self["num-items"]) / float(cols))
		else:
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
				
