from gestalt.Type import *
from gestalt.nodes.Node import Node

class PolylineNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.points = layout.pop("points", [])
		
		super(PolylineNode, self).__init__("Polyline", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
		
		self.tocopy.append("points")
		
