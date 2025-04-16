from gestalt.Type import *
from gestalt.nodes.Node import Node
from gestalt.nodes.GroupNode import GroupNode

class EmbedNode(GroupNode):
	def __init__(self, name=None, layout={}, loc=None):
		super(EmbedNode, self).__init__("Embed", name=name, layout=layout, loc=loc)
	
	def initApply(self, data):
		self.children = []
		
		for item in List(data.get(str(self["embedding"]), [])):
			if isinstance(item, Node):
				self.append(item, keep_original=True)
