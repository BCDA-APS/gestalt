import yaml
import copy
import math
import string


from gestalt.Type import *


class Node(object):
	def __init__(self, classname, name=None, layout=None):
		self.classname = classname
		self.name = None
		
		self.attrs = {"geometry" : Rect(x=0, y=0, width=0, height=0)}
		
		if name is not None:
			self.name = name
		
		if layout is not None:
			self.setProperties(layout)
						
					
	def setProperty(self, key, data):
		to_assign = None
		
		if isinstance(data, DataType):
			to_assign = data
		elif isinstance(data, bool):
			to_assign = Bool(data)
		elif isinstance(data, int):
			to_assign = Number(data)
		elif isinstance(data, float):
			to_assign = Double(data)
		elif isinstance(data, dict):
			to_assign = DataType(data)
		elif isinstance(data, str):
			to_assign = yaml.safe_load(data)
			
			if not isinstance(to_assign, DataType):
				to_assign = String(data)
			
			
		if key in self.attrs:
			self.attrs[key] = self.attrs[key].merge(to_assign)
		else:
			self.attrs[key] = to_assign

		return self
	
		
	def setProperties(self, *args, **kwargs):
		if len(args) != 0:
			for key, val in args[0].items():
				self.setProperty(key, val)
			
		if kwargs:
			for key, val in kwargs.items():
				self.setProperty(key, val)
			
		return self
	
		
	def getProperty(self, key):
		return self.attrs[key]
		
		
	def __setitem__(self, key, data):
		self.setProperty(key, data)			
		
		
	def __getitem__(self, key):
		return self.getProperty(key)
		
		
	def position(self, *args, x=None, y=None):
		out_x = 0
		out_y = 0
			
		if len(args) == 2:
			out_x = args[0]
			out_y = args[1]
			
		elif x is not None:
			out_x = x
			out_y = y
			
		elif len(args) == 1:
			if isinstance(args[0], list) or isinstance(args[0], tuple):
				out_x = args[0][0]
				out_y = args[0][1]
			elif isinstance(args[0], dict):
				out_x = args[0]["x"]
				out_y = args[0]["y"]				
		
		self.setProperty("geometry", Rect(x = out_x, y = out_y))
				
		return self

		
	def apply (self, generator, data={}):		
		return generator.generateWidget(self, macros=data)
		
		
		
class GroupNode(Node):
	def __init__(self, classname, initial=None, name=None, layout=None):
		super(GroupNode, self).__init__(classname, name=name, layout=layout)
	
		self.margins = Rect(x=0, y=0, width=0, height=0)
		self.margins = self.margins.merge(self.attrs.get("margins", Rect(x=0, y=0, width=0, height=0)))
	
		self.children = []
		
		if initial is not None:
			if isinstance(initial, dict):
				for childname, child in initial.items():
					child.name = childname
					self.append(child)
				
			elif isinstance(initial, list) or isinstance(initial, tuple):
				for child in initial:
					self.append(child)
	
					
	def append(self, child, keep_original=False):	
		if not keep_original:
			self.children.append(copy.deepcopy(child))
		else:
			self.children.append(child)
		
		child["geometry"]["x"] = child["geometry"]["x"] + self.margins["x"]
		child["geometry"]["y"] = child["geometry"]["y"] + self.margins["y"]
			
		right_edge  = child["geometry"]["x"] + child["geometry"]["width"] + self.margins["width"]
		bottom_edge = child["geometry"]["y"] + child["geometry"]["height"] + self.margins["height"]
		
		if right_edge > self["geometry"]["width"]:
			self["geometry"]["width"] = right_edge
			
		if bottom_edge > self["geometry"]["height"]:
			self["geometry"]["height"] = bottom_edge
			
		return self
		
	
	def apply (self, generator, data={}):
		output = generator.generateGroup(self, macros=data)
				
		child_macros = copy.deepcopy(data)
		
		for child in self.children:
			child_macros.update({
				"__parentx__" : output["geometry"]["x"],
				"__parenty__" : output["geometry"]["y"],
				"__parentwidth__" : output["geometry"]["width"],
				"__parentheight__" : output["geometry"]["height"]})
				
			output.append(child.apply(generator, data=child_macros))
			
		return output

		
class GridNode(GroupNode):
	def __init__(self, initial=None, name=None, layout=None, padding=0, repeat=None, ratio=1.0):
		super(GridNode, self).__init__("caFrame", initial=initial, name=name, layout=layout)
		
		self.ratio = ratio
		self.repeat_over = repeat
		self.padding = padding
		
		
	def apply (self, generator, data={}):
		macrolist = data.get(self.repeat_over, {})
		
		output = generator.generateGroup(self, macros=data)
		
		num_items = len(macrolist)
		
		cols = round(math.sqrt(num_items * self.ratio))
		rows = round(math.sqrt(num_items / self.ratio))
		
		index = 0
		index_x = 0
		index_y = 0
		
		for macroset in macrolist:
			child_macros = copy.deepcopy(data)
			child_macros.update(macroset)
			child_macros.update({"__index__" : index})
			
			element = generator.generateAnonymousGroup()
			
			for childnode in self.children:
				child_macros.update({
					"__parentx__" : output["geometry"]["x"],
					"__parenty__" : output["geometry"]["y"],
					"__parentwidth__" : output["geometry"]["width"],
					"__parentheight__" : output["geometry"]["height"]})
					
				element.append(childnode.apply(generator, data=child_macros))
			
			pos_x = index_x * (element["geometry"]["width"] + self.padding)
			pos_y = index_y * (element["geometry"]["height"] + self.padding)
				
			element.position(pos_x, pos_y)
			
			index += 1
			index_x += 1
			
			if index_x >= cols:
				index_x = 0
				index_y += 1
		
			output.append(element)
			
		return output
		
		
class RepeatNode(GroupNode):
	def __init__(self, initial=None, name=None, layout=None, repeat=None, padding=0, flow="vertical"):
		super(RepeatNode, self).__init__("caFrame", initial=initial, name=name, layout=layout)
		
		self.repeat_over = repeat
		self.padding = padding
		self.flow = flow
	
		
	def apply (self, generator, data={}):		
		macrolist = data.get(self.repeat_over, None)
		
		output = generator.generateGroup(self, macros=data)
		
		index = 0
		
		if not isinstance(macrolist, list):
			if isinstance(macrolist, DataType):
				macrolist = [ {"N" : x} for x in range(int(macrolist.val)) ]
			else:
				macrolist = [ {"N" : x} for x in range(int(macrolist)) ]
		
		for macroset in macrolist:
			child_macros = copy.deepcopy(data)
			child_macros.update(macroset)
			child_macros.update({"__index__" : index})
			
			line = generator.generateAnonymousGroup()
			
			for childnode in self.children:
				child_macros.update({
					"__parentx__" : self["geometry"]["x"],
					"__parenty__" : self["geometry"]["y"],
					"__parentwidth__" : self["geometry"]["width"],
					"__parentheight__" : self["geometry"]["height"]})
					
				line.append(childnode.apply(generator, data=child_macros))
			
				
			if self.flow == "vertical":
				line.position(x=0, y=(index * (line["geometry"]["height"] + self.padding)))
				
			elif self.flow == "horizontal":
				line.position(x=(index * (line["geometry"]["width"] + self.padding)), y=0)
				
			output.append(line)
			index += 1
			
		return output


class ConditionalNode(GroupNode):
	def __init__(self, initial=None, name=None, layout=None, condition=None):
		super(ConditionalNode, self).__init__("caFrame", initial=initial, name=name, layout=layout)
		
		self.condition = condition
		
	def apply(self, generator, data={}):
		output = generator.generateAnonymousGroup()
		
		conditional = data.get(self.condition, None)
		
		if bool(conditional):
			child_macros = copy.deepcopy(data)
			
			for childnode in self.children:
				child_macros.update({
					"__parentx__" : self["geometry"]["x"],
					"__parenty__" : self["geometry"]["y"],
					"__parentwidth__" : self["geometry"]["width"],
					"__parentheight__" : self["geometry"]["height"]})
				
				output.append(childnode.apply(generator, data=data))
		
		return output
		
		
class StretchNode(Node):
	def __init__(self, name=None, layout=None, flow="vertical", subnode=None):
		super(StretchNode, self).__init__("Stretch", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def apply (self, generator, data={}):
		if self.flow == "vertical":
			self.subnode["geometry"]["height"] = data["__parentheight__"]
		elif self.flow == "horizontal":
			self.subnode["geometry"]["width"] = data["__parentwidth__"]
		
		return self.subnode.apply(generator, data=data)

		
class CenterNode(Node):
	def __init__(self, name=None, layout=None, flow="vertical", subnode=None):
		super(CenterNode, self).__init__("Center", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def apply (self, generator, data={}):
		applied_node = self.subnode.apply(generator, data=data)
			
		if self.flow == "vertical":
			applied_node.position(applied_node["geometry"]["x"], int(data["__parentheight__"] / 2) - int(applied_node["geometry"]["height"] / 2))
		elif self.flow == "horizontal":
			applied_node.position(int(data["__parentwidth__"] / 2) - int(applied_node["geometry"]["width"] / 2), applied_node["geometry"]["y"])
					
		return applied_node	
