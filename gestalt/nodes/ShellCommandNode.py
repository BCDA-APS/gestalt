from gestalt.Type import *
from gestalt.nodes.Node import Node

class ShellCommandNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.proto_commands = List(layout.pop("proto_commands", []))
	
		super(ShellCommandNode, self).__init__("ShellCommand", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,    "text",       "")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",  "Center")
		
		self.makeInternal(List, "commands", [])
		
		self.tocopy.append("proto_commands")

			
	def initApply(self, macros):
		copy_commands = copy.deepcopy(self.proto_commands)
		copy_commands.apply(macros)
		
		output = []
		
		for item in copy_commands:
			a_command = Dict(item)
			a_command.apply(macros)
			output.append(a_command.val())
			
		self["commands"] = List(output)
