from gestalt.Type import *
from gestalt.nodes.Node import Node

class TextNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(TextNode, self).__init__("Text", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,     "foreground",   "$000000")
		self.setDefault(Color,     "background",   "$00000000")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(String,    "border-style", "Solid")
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",    "CenterLeft")
