from gestalt.Type import *
from gestalt.nodes.Node import Node

class RelatedDisplayNode(Node):
	def __init__(self, name=None, layout={}, loc=None):		
		self.links = layout.pop("links", [])
	
		super(RelatedDisplayNode, self).__init__("RelatedDisplay", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,    "text",       "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Alignment, "alignment",  "Center")
		
		self.tocopy.append("links")
	
		if isinstance(self.links, dict):
			temp = []
			
			for key, val in self.links.items():
				val["label"] = key
				temp.append(val)
				
			self.links = temp
