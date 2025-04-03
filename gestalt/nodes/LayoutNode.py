from gestalt.Type import *
from gestalt.nodes.GroupNode import GroupNode

class LayoutNode(GroupNode):
	def __init__(self, name=None, layout={}, loc=None):
		super(LayoutNode, self).__init__("Layout", name=name, layout=layout, loc=loc)
		
		self.makeInternal(String, "repeat-over",  "")
		self.makeInternal(String, "variable",     "N")
		self.makeInternal(Number, "start-at",     0)
		self.makeInternal(Number, "padding",      0)
		
		self.makeInternal(Number, "index",     0)
		self.makeInternal(Number, "num-items", 0)
		self.makeInternal(Number, "last-x",    0)
		self.makeInternal(Number, "last-y",    0)
		
	def initApply(self, data):
		self["index"] = 0
		self["last-x"] = 0
		self["last-y"] = 0
		self["padding"].apply(data)
		
		self["repeat-over"].apply(data)
		self["start-at"].apply(data)
		self["variable"].apply(data)
		
		self.data = data
		
	def updateMacros(self, child_macros):
		super().updateMacros(child_macros)
		
		child_macros.update({"__index__"   : self["index"].val()})
		child_macros.update({str(self["variable"]) : int(self["index"].val()) + int(self["start-at"].val())})
		child_macros.update(self.curr_macros)
		
		
	def __iter__(self):
		repeat   = self["repeat-over"]
		start_at = self["start-at"]
		value_var = self["variable"]
		
		macrolist = self.data.get(str(repeat))
		
		try:
			if not macrolist:
				macrolist = range(int(start_at), int(start_at) + int(repeat))
			elif not isinstance(macrolist, list):
				macrolist = range(int(start_at), int(start_at) + int(macrolist))
		except:
			macrolist = List(repeat)
			macrolist.apply(self.data)
			macrolist = macrolist.val()
		
		
		if not macrolist:
			raise Exception("Could not resolve repeat-over (" + str(repeat) + ") into an iterable value")
			
		self["num-items"] = len(macrolist)
		
		if macrolist:
			for item in macrolist:
				if isinstance(item, dict):
					self.curr_macros = item
				else:
					self.curr_macros = {str(value_var) : item}
					
				line = GroupNode(anonymous=True)
				
				for childnode in super().__iter__():
					line.append(childnode)
					
				yield line
				
				self["index"] = self["index"].val() + 1
