from gestalt.Type import *
from gestalt.nodes.Node import Node

class ArcNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ArcNode, self).__init__("Arc", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
		self.setDefault(Number, "start-angle", 0)
		self.setDefault(Number, "span", 90)
