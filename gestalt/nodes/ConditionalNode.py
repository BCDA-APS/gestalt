from gestalt.Type import *

from gestalt.nodes.GroupNode import GroupNode

class ConditionalNode(GroupNode):
	def __init__(self, layout={}, loc=None):
		super(ConditionalNode, self).__init__("caFrame", layout=layout, loc=loc)
		
		self.condition = self.pop("condition", "")
		
		for item in self:
			self["render-order"] = max(int(item["render-order"]), int(self["render-order"]))
			self["z-order"]      = max(int(item["z-order"]), int(self["z-order"]))
		
		self.tocopy.append("condition")
		
	
	def apply(self, generator):
		data = yield
		
		output = generator.generateAnonymousGroup()
		output.position(x=self["geometry"]["x"], y=self["geometry"]["y"])

		invert = isinstance(self.condition, Not)
		
		my_condition = String(self.condition)
		my_condition.apply(data)
		
		conditional = None
		
		try:
			conditional = data[str(my_condition)]
		except KeyError:
			if "{" in my_condition.value:
				conditional = str(my_condition)

		if bool(conditional) != invert:		
			for childnode in self.children:
				applier = childnode.apply(generator)
				
				for increment in applier:
					try:
						widget = applier.send(data)
						output.place(widget)
					except:
						break
				
			if len(output.children):
				yield output
				return
			
		yield None
