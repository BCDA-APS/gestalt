from gestalt.Type import *
from gestalt.nodes.Node import Node

class ScaleNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ScaleNode, self).__init__("Scale", name=name, layout=layout, loc=loc)
		
		self.setDefault(String, "pv",          "")
		self.setDefault(Color,  "background",  "$C0C0C0")
		self.setDefault(Color,  "foreground",  "$0000FF")
		self.setDefault(Bool,   "horizontal",  False)
