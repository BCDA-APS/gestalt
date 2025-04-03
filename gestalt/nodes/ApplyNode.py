from gestalt.Type import *
from gestalt.nodes.GroupNode import GroupNode

class ApplyNode(GroupNode):
	def __init__(self, layout={}, defaults={}, macros={}, subnodes=[], loc=None):
		super(ApplyNode, self).__init__("Apply", layout=layout, loc=loc, anonymous=True)
		
		self.defaults = defaults
		self.macros = macros
		
		for item in self:
			self["render-order"] = max(int(item["render-order"]), int(self["render-order"]))
			self["z-order"]      = max(int(item["z-order"]), int(self["z-order"]))
		
		self.tocopy.append("macros")
		self.tocopy.append("defaults")
		
	def initApply(self, data):
		super().initApply(data)
		self.data = data
		
	def updateMacros(self, child_macros):
		super().updateMacros(child_macros)
		
		macro_list = {}
		
		macro_list.update(self.defaults)
		macro_list.update(self.data)
		macro_list.update(self.macros)
		
		less = {}
		less.update(self.defaults)
		less.update(self.macros)
		
		for key, val in macro_list.items():
			to_assign = None
			
			if isinstance(val, bool):
				to_assign = Bool(val)
			elif isinstance(val, int):
				to_assign = Number(val)
			elif isinstance(val, float):
				to_assign = Double(val)
			elif isinstance(val, str):
				to_assign = String(val)
			else:
				to_assign = val
			
			if isinstance(to_assign, DataType):
				to_assign.apply(less)				
				to_assign = to_assign.flatten()
				to_assign.apply(self.data)
				
			child_macros.update({key : to_assign})
