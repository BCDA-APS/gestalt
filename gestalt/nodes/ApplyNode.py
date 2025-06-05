from gestalt.Type import *
from gestalt.nodes.GroupNode import GroupNode

class ApplyNode(GroupNode):
	def __init__(self, template="", layout={}, defaults={}, macros={}, subnodes=[], loc=None):
		super(ApplyNode, self).__init__("Apply", layout=layout, loc=loc, anonymous=True)
				
		self.defaults = defaults
		self.macros = macros
		
		self.template = template
		
		for item in self:
			self["render-order"] = max(int(item["render-order"]), int(self["render-order"]))
			self["z-order"]      = max(int(item["z-order"]), int(self["z-order"]))
		
		self.tocopy.append("macros")
		self.tocopy.append("defaults")
		self.tocopy.append("template")
		
	def initApply(self, data):
		super().initApply(data)
		self.data = data
		
	def updateMacros(self, output, macros):		
		super().updateMacros(output, macros)
		
		output = {}
		output.update(self.defaults)
		output.update(self.data)
		output.update(self.macros)
		
		to_apply = {}
		to_apply.update(self.defaults)
		to_apply.update(self.macros)
		to_apply.update(self.data)
		
		for key, val in output.items():
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
				to_assign.apply(to_apply)
				to_assign = to_assign.flatten()
				#to_assign.apply(self.data)
				
			macros.update({key : to_assign})
					
		return
