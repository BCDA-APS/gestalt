from gestalt.nodes.Node import Node

class CenterNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None, loc=None):
		super(CenterNode, self).__init__("Center", name=name, layout=layout, loc=loc)
		
		self.setProperty("flow", flow, internal=True)
		self.setProperty("render-order", 1)
		
		self.subnode = subnode
		self.tocopy.append("subnode")
		
	
	def apply (self, generator):
		data = yield
		
		if self.name:
			self.subnode.name = self.name
		
		flow = self["flow"].val()
		
		applier = self.subnode.apply(generator)
		applied_node = None
		
		index = 0
		
		for increment in applier:			
			applied_node = applier.send(data)
			applied_node.placed_order = self.placed_order
				
			yield applied_node
			
			# Adjust position of previously returned node (accounts for size changes of parent widget by getting the next set of macros)
			data = yield
			
			if flow == "vertical":
				applied_node.position(x=applied_node["geometry"]["x"] + self["geometry"]["x"], y=int(data["__parentcentery__"]) - int(int(applied_node["geometry"]["height"]) / 2))
			elif flow == "horizontal":
				applied_node.position(x=int(data["__parentcenterx__"]) - int(int(applied_node["geometry"]["width"]) / 2), y=applied_node["geometry"]["y"] + self["geometry"]["y"])
			elif flow == "all":
				applied_node.position(x=int(data["__parentcenterx__"]) - int(int(applied_node["geometry"]["width"]) / 2), y=int(data["__parentcentery__"]) - int(int(applied_node["geometry"]["height"]) / 2))
