from gestalt.Type import *
from gestalt.nodes.Node import Node

class LEDNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(LEDNode, self).__init__("LED", name=name, layout=layout, loc=loc)
	
		self.setDefault(String, "pv",             "")
		self.setDefault(Bool,   "square",         False)
	
		self.setDefault(Color, "false-color",     "$3C643C")
		self.setDefault(Color, "true-color",      "$00FF00")
		self.setDefault(Color, "undefined-color", "$A0A0A4")
		self.setDefault(Color, "border-color",    "$000000")
	
		self.setDefault(Number, "false-value", 0)
		self.setDefault(Number, "true-value", 1)
