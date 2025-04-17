from gestalt.Type import *
from gestalt.nodes.Node import Node
from gestalt.nodes.GroupNode import GroupNode

class EmbedNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(EmbedNode, self).__init__("Embed", name=name, layout=layout, loc=loc)
	
	def apply(self, generator):
		data = yield
		
		children = []
		
		for item in List(data.get(str(self["embedding"]), [])):			
			if isinstance(item, Node):
				children.append(item)
				
		for child in children:
			applier = child.apply(generator)
			
			for increment in applier:
				child_macros = copy.copy(data)
				
				try: 
					widget = applier.send(child_macros)
					
					yield widget
				except:
					break
					
				data = yield
