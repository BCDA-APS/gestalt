import copy

from gestalt.nodes.Node import Node

class StretchNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None, loc=None):
		super(StretchNode, self).__init__("Stretch", name=name, layout=layout, loc=loc)
				
		self.setProperty("flow", flow, internal=True)
		self.setProperty("render-order", 1)
		
		self.subnode = subnode
		self.tocopy.append("subnode")
		
	
	def apply (self, generator):
		the_node = copy.deepcopy(self.subnode)
		
		if self.name:
			the_node.name = self.name
		
		applier = the_node.apply(generator)
		
		for increment in applier:
			data = yield
			
			flow = self["flow"].val()
			
			if flow == "vertical" or flow == "all":
				the_node["geometry"]["height"] = data["__parentheight__"]
			if flow == "horizontal" or flow=="all":
				the_node["geometry"]["width"] = data["__parentwidth__"]
			
			applied_node = applier.send(data)
			applied_node.placed_order = self.placed_order
			
			yield applied_node
