from gestalt.Type import *
from gestalt.nodes.Node import Node

class EllipseNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(EllipseNode, self).__init__("Ellipse", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
