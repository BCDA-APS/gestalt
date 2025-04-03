from gestalt.nodes.Node import Node

class AnchorNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None, loc=None):
		super(AnchorNode, self).__init__("Anchor", name=name, layout=layout, loc=loc)
		
		self.setProperty("flow", flow, internal=True)
		self.setProperty("render-order", 1)
		
		self.subnode = subnode
		self.tocopy.append("subnode")
	
	def apply (self, generator):
		if self.name:
			self.subnode.name = self.name
			
		flow = self["flow"].val()
			
		applier = self.subnode.apply(generator)
		
		for increment in applier:
			data = yield
			
			applied_node = applier.send(data)
			applied_node.placed_order = self.placed_order
			
			if flow == "vertical":
				applied_node.position(x=applied_node["geometry"]["x"] + self["geometry"]["x"], y=int(data["__parentheight__"]) - int(applied_node["geometry"]["height"]))
			elif flow == "horizontal":
				applied_node.position(x=int(data["__parentwidth__"]) - int(applied_node["geometry"]["width"]), y=applied_node["geometry"]["y"] + self["geometry"]["y"])
			elif flow == "all":
				applied_node.position(x=int(data["__parentwidth__"]) - int(applied_node["geometry"]["width"]), y=int(data["__parentheight__"]) - int(applied_node["geometry"]["height"]))
			
			yield applied_node	
