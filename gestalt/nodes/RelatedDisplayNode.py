import pathlib

from gestalt.Type import *
from gestalt.nodes.Node import Node

class RelatedDisplayNode(Node):
	def __init__(self, name=None, layout={}, loc=None):	
		super(RelatedDisplayNode, self).__init__("RelatedDisplay", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,    "text",       "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Alignment, "alignment",  "Center")
		
		self.makeInternal(List, "links", [])

			
	def initApply(self, macros):
		self["links"].apply(macros)
		
		output = []
		
		for item in self["links"]:
			a_link = Dict(item)
			a_link.apply(macros)
			a_link = a_link.val()
		
			filename = a_link.get("file", "")
			
			a_link["file"] = filename.removesuffix(pathlib.PurePath(filename).suffix)
			output.append(a_link)
			
		self["links"] = List(output)
		
