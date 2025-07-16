import yaml

from gestalt.Type import *
from gestalt.nodes.GroupNode import GroupNode

class LayoutNode(GroupNode):
	def __init__(self, classname="Layout", name=None, layout={}, loc=None):
		super(LayoutNode, self).__init__(classname, name=name, layout=layout, loc=loc)
		
		self.makeInternal(String, "repeat-over",  "")
		self.makeInternal(String, "variable",     "N")
		self.makeInternal(Number, "start-at",     0)
		self.makeInternal(Number, "padding",      0)
		self.makeInternal(Number, "increment",    1)
		
		self.makeInternal(Number, "index",     0)
		self.makeInternal(Number, "num-items", 0)
		self.makeInternal(Number, "last-x",    0)
		self.makeInternal(Number, "last-y",    0)
		
		self.makeInternal(Bool, "reverse", False)
		
	def initApply(self, data):
		self["last-x"] = 0
		self["last-y"] = 0
		self["padding"].apply(data)
		
		self["repeat-over"].apply(data)
		self["start-at"].apply(data)
		self["variable"].apply(data)
		self["increment"].apply(data)
		
		self["reverse"].apply(data)
		
		self.data = data
		
	def updateMacros(self, output, macros):
		super().updateMacros(output, macros)
		
		macros.update({"__index__"   : self["index"]})
		macros.update({str(self["variable"]) : self.iterating[self["index"].val()]})
		macros.update(self.curr_macros)
		
		
	def __iter__(self):
		repeat    = self["repeat-over"]
		start_at  = int(self["start-at"])
		value_var = str(self["variable"])
		inc_val   = int(self["increment"])

		self.iterating = None
		
		check = repeat.val()
		
		if isinstance(check, str):
			check = DataType(None, self.data.get(check, check)).val()
			
		if isinstance(check, str):
			check = yaml.safe_load(check)
			
		if isinstance(check, dict):
			check = Dict(check)
			check.apply(self.data)
			self.iterating = check.val()
			
		elif isinstance(check, list):
			check = List(check)
			check.apply(self.data)
			
			self.iterating = dict(enumerate(check.val()))
			
		else:
			try:
				self.iterating = dict( enumerate( range(start_at, start_at + (int(check) * inc_val), inc_val)))
			except Exception as e:
				pass
				
		if not self.iterating:
			raise Exception("Could not resolve repeat-over (" + str(repeat) + ") into an iterable value")
						
		self["num-items"] = len(self.iterating)
		
		the_iter = self.iterating.items()
		
		if bool(self["reverse"]):
			the_iter = reversed(the_iter)
		
		for key, val in the_iter:
			self["index"] = key
			self.curr_macros = {}
			
			if isinstance(val, dict):				
				self.curr_macros = val
			else:
				test = Dict(val)
				test.apply(self.data)
				check = test.val()
				
				if isinstance(check, dict):
					self.curr_macros = check
					
			line = GroupNode(anonymous=True)
			line["ignore-empty"] = self["ignore-empty"]
			
			for childnode in super().__iter__():
				line.append(childnode)
				
			yield line
				
