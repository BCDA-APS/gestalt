from gestalt.Type import *
from gestalt.nodes.Node import Node

class TextEntryNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(TextEntryNode, self).__init__("TextEntry", name=name, layout=layout, loc=loc)
	
		self.setDefault(String,    "pv",         "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(String,    "format",     "Decimal")
		self.setDefault(Alignment, "alignment",  "CenterLeft")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Color,     "foreground", "$000000")
