from gestalt.Type import *
from gestalt.nodes.Node import Node

class MessageButtonNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(MessageButtonNode, self).__init__("MessageButton", name=name, layout=layout, loc=loc)
		self.setDefault(String,    "text",       "")
		self.setDefault(String,    "pv",         "")
		self.setDefault(String,    "value",      "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Alignment, "alignment",  "Center")
