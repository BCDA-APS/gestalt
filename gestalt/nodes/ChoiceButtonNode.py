from gestalt.Type import *
from gestalt.nodes.Node import Node

class ChoiceButtonNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ChoiceButtonNode, self).__init__("ChoiceButton", name=name, layout=layout, loc=loc)
	
		self.setDefault(String, "pv",         "")
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(Color,  "background", "$C8C8C8")
		self.setDefault(Color,  "selected",   self["background"])
