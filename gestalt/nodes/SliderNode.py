from gestalt.Type import *
from gestalt.nodes.Node import Node

class SliderNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(SliderNode, self).__init__("Slider", name=name, layout=layout, loc=loc)
		
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(String, "pv",         "")
		

