from gestalt.nodes.Node import Node

class SpacerNode(Node):
	def __init__(self, layout={}, loc=None):
		super(SpacerNode, self).__init__("Spacer", layout=layout, loc=loc)
	
	
	def apply(self, generator):
		data = yield
		
		output = generator.generateAnonymousGroup()
		output["geometry"] = self["geometry"]
		output["geometry"].apply(data)
		
		yield output
		
