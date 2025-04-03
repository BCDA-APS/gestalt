from gestalt.Type import *
from gestalt.nodes.Node import Node

class ByteMonitorNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ByteMonitorNode, self).__init__("ByteMonitor", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,  "pv",          "")
		self.setDefault(Bool,    "horizontal",  True)
		self.setDefault(Number,  "start-bit",   0)
		self.setDefault(Number,  "bits",        (32 - int(self["start-bit"])))
		self.setDefault(Color,   "off-color",   "$3C643C")
		self.setDefault(Color,   "on-color",    "$00FF00")
