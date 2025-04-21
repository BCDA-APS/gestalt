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
			for child in self.children:				
				applier = child.apply(generator)
				
				for increment in applier:
					child_macros = copy.copy(data)
					
					try:
						widget = applier.send(child_macros)
						yield widget
					except:
						break
				
					data = yield
