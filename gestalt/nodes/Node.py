import copy
import pprint

from gestalt.Generator import GestaltGenerator
from gestalt.Type import *

class Node(object):
	def __init__(self, classname, name=None, node=None, layout={}, loc=None):
		self.classname = classname
		self.name = name
		self.location = loc
		self.debug = False
		self.placed_order = None
		
		self.properties = {}
		self.properties["attrs"] = {}
		self.properties["internal"]  = {}
		
		self.tocopy = []
		
		if node:
			self.name = node.name
			self.location = node.location
			self.debug = node.debug
			self.placed_order = node.placed_order
			
			for typ in ( "attrs", "internal" ):
				for key,val in node.properties[typ].items():
					if isinstance(val, DataType):
						self.properties[typ][key] = val.copy()
					else:
						# Profiling shows this to not come up
						self.properties[typ][key] = copy.deepcopy(val)
		else:
			if layout is not None:
				for key, val in layout.items():
					self.setProperty(key, val)
		
			
		self.setDefault(Rect, "geometry", "0x0x0x0")
		self.makeInternal(Number, "render-order", 0)
		self.makeInternal(Number, "z-order", 0)
	
		
	def log(self, info):
		if self.debug:
			print(str(self.name) + ": " + info)
			
	def setDefault(self, datatype, key, default, internal=False):
		which = "internal" if internal else "attrs"
		self.properties[which][key] = datatype(self.properties[which].pop(key, default))
	
	def makeInternal(self, datatype, key, default=None):
		self.setDefault(datatype, key, self.properties["attrs"].pop(key, default), internal=True)
		
	def link(self, newkey, oldkey, conversion=None):
		which = "internal" if oldkey in self.properties["internal"] else "attrs"
				
		olddata = self.properties[which].pop(oldkey)
			
		if conversion:
			check_str = olddata.val()

			if (check_str in conversion):
				olddata = conversion[check_str]
			else:
				print ("Invalid format: {name}".format(name=check_str))
				return None

		self.properties[which][newkey] = olddata
		
		
	def pop(self, key, default=None):
		if key in self.properties["internal"]:
			return self.properties["internal"].pop(key, default)
		else:
			return self.properties["attrs"].pop(key, default)
		
	def updateProperties(self, macros={}):
		if len(macros) == 0: return
		
		self.log("Updating macros\n" + pprint.pformat(macros))
			
		for attr in self.properties["internal"].values():
			attr.apply(macros)
		
		for attr in self.properties["attrs"].values():
			attr.apply(macros)
			
			
	def setProperty(self, key, input, internal=False):
		to_assign = None
		
		if isinstance(input, bool):
			to_assign = Bool(input)
		elif isinstance(input, int):
			to_assign = Number(input)
		elif isinstance(input, float):
			to_assign = Double(input)
		elif isinstance(input, str):
			to_assign = String(input)
		elif isinstance(input, list):
			to_assign = []
			for item in input:
				to_assign.append(copy.copy(item))
		elif isinstance(input, DataType):
			to_assign = input.copy()
		else:
			to_assign = copy.deepcopy(input)

		which = "internal" if key in self.properties["internal"] else "attrs"
			
		if isinstance(to_assign, DataType):
			self.log("Setting Property " + key + " from " + str(self.properties[which].get(key)) + " to " + str(to_assign.value))
		else:
			self.log("Setting Property " + key + " from " + str(self.properties[which].get(key)) + " to " + pprint.pformat(to_assign))
			
		self.properties[which][key] = to_assign
		
		
	def getProperty(self, key, internal=False):
		if internal or key not in self:
			return self.properties["internal"][key]
		else:
			return self.properties["attrs"][key]
		
		
	def __setitem__(self, key, data):		
		self.setProperty(key, data)	
		
	def __getitem__(self, key):
		return self.getProperty(key)
		
	def __contains__(self, key):
		return key in self.properties["attrs"]
		
		
	def position(self, x=None, y=None):
		if x is not None:
			self.log("Setting x to " + str(x))
			self["geometry"]["x"] = x
		
		if y is not None:
			self.log("Setting y to " + str(y))
			self["geometry"]["y"] = y
				
		return self

		
	def initApply(self, data):
		pass
	
	def apply (self, generator):
		data = yield
		
		self.initApply(data)
		
		gen_func = getattr(generator, "generate" + self.classname, None)
		
		if gen_func:
			self.log("Generating " + self.classname)
			yield gen_func(self, macros=data)
		else:
			self.log("Generating generic widget")
			yield generator.generateWidget(self, macros=data)
			
			
	def __deepcopy__(self, memo):
		cls = self.__class__
		output = cls.__new__(cls)
		
		output.classname = self.classname
		output.name = self.name
		output.location = self.location
		output.debug = self.debug
		output.placed_order = self.placed_order
		
		output.properties = {}
		output.properties["attrs"] = copy.copy(self.properties["attrs"])
		output.properties["internal"] = copy.copy(self.properties["internal"])
		
		output.tocopy = copy.copy(self.tocopy)

		for attr in self.tocopy:
			setattr(output, attr, copy.deepcopy(getattr(self, attr), memo))
		
		memo[id(self)] = output
		
		return output
