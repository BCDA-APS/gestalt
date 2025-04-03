from gestalt.Type import *
from gestalt.nodes.Node import Node

class MenuNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(MenuNode, self).__init__("Menu", name=name, layout=layout, loc=loc)
	
		self.setDefault(String, "pv", "")
		self.setDefault(Color, "background", "$57CAE4")
		self.setDefault(Color, "foreground", "$000000")
