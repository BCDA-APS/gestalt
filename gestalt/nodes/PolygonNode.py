from gestalt.Type import *
from gestalt.nodes.Node import Node

class PolygonNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.points = layout.pop("points", [])
		
		super(PolygonNode, self).__init__("Polygon", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
		
		self.tocopy.append("points")

