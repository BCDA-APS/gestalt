from gestalt.Type import *
from gestalt.nodes.Node import Node

class RectangleNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(RectangleNode, self).__init__("Rectangle", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
