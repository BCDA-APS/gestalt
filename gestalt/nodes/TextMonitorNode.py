from gestalt.Type import *
from gestalt.nodes.Node import Node

class TextMonitorNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(TextMonitorNode, self).__init__("TextMonitor", name=name, layout=layout, loc=loc)
	
		self.setDefault(String,    "pv",           "")
		self.setDefault(Color,     "foreground",   "$000000")
		self.setDefault(Color,     "background",   "$00000000")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(String,    "border-style", "Solid")
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(String,    "format",       "Decimal")
		self.setDefault(Alignment, "alignment",    "CenterLeft")
