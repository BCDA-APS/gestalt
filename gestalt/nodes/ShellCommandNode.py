from gestalt.Type import *
from gestalt.nodes.Node import Node

class ShellCommandNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.commands = layout.pop("commands", [])
	
		super(ShellCommandNode, self).__init__("ShellCommand", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,    "text",       "")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",  "Center")
		
		self.tocopy.append("commands")
	
		if isinstance(self.commands, dict):
			temp = []
			
			for key, val in self.commands.items():
				val["label"] = key
				temp.append(val)
				
			self.commands = temp
