from gestalt.Type import *
from gestalt.nodes.Node import Node

class ImageNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ImageNode, self).__init__("Image", name=name, layout=layout, loc=loc)
		
		self.setDefault(String, "file", "")
