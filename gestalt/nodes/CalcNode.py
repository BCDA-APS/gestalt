from gestalt.Type import *
from gestalt.nodes.Node import Node

class CalcNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(CalcNode, self).__init__("Calc", name=name, layout=layout, loc=loc)

		self.setDefault(String, "pv", "")
		self.setDefault(String, "A", "")
		self.setDefault(String, "B", "")
		self.setDefault(String, "C", "")
		self.setDefault(String, "D", "")
		self.setDefault(String, "calc", "")
