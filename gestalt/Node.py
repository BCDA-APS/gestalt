import yaml
import copy
import math
import string


from gestalt.Type import *


class Node(object):
	def __init__(self, classname, name=None, layout={}):
		self.classname = classname
		self.name = None
		
		self.attrs = {"geometry" : Rect(x=0, y=0, width=0, height=0)}
		
		if name is not None:
			self.name = name
		
		if layout is not None:
			Node.setProperties(self, layout)
						
					
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
		out_x = None
		out_y = None
			
		if len(args) == 2:
			out_x = args[0]
			out_y = args[1]
			
		
		if x is not None:
			out_x = x
			
		if y is not None:
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
	def __init__(self, classname, name=None, layout={}):
		initial = layout.pop("children", {})
	
		super(GroupNode, self).__init__(classname, name=name, layout=layout)
	
		self.margins = Rect(x=0, y=0, width=0, height=0)
		self.margins = self.margins.merge(self.attrs.get("margins", Rect(x=0, y=0, width=0, height=0)))
	
		self.children = []
		
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
			
		return self
		
		
	def place(self, child, x=None, y=None, keep_original=False):
		self.append(child, keep_original=keep_original)
		
		child_node = self.children[-1]
		
		if x:
			child_node["geometry"]["x"] = x + self.margins["x"]
		else:
			child_node["geometry"]["x"] = child_node["geometry"]["x"] + self.margins["x"]
			
		if y:
			child_node["geometry"]["y"] = y + self.margins["y"]
		else:
			child_node["geometry"]["y"] = child_node["geometry"]["y"] + self.margins["y"]
		
		right_edge  = child_node["geometry"]["x"] + child_node["geometry"]["width"] + self.margins["width"]
		bottom_edge = child_node["geometry"]["y"] + child_node["geometry"]["height"] + self.margins["height"]
		
		if right_edge > self["geometry"]["width"]:
			self["geometry"]["width"] = right_edge
			
		if bottom_edge > self["geometry"]["height"]:
			self["geometry"]["height"] = bottom_edge
		
	
	def apply (self, generator, data={}):
		output = generator.generateGroup(self, macros=data)
				
		child_macros = copy.deepcopy(data)
		
		for child in self.children:
			child_macros.update({
				"__parentx__" : output["geometry"]["x"],
				"__parenty__" : output["geometry"]["y"],
				"__parentwidth__" : output["geometry"]["width"],
				"__parentheight__" : output["geometry"]["height"]})
						
			output.place(child.apply(generator, data=child_macros))
			
		return output

		
class GridNode(GroupNode):
	def __init__(self, name=None, layout={}):
		super(GridNode, self).__init__("caFrame", layout=layout)
	
		self.ratio = self.attrs.pop("aspect_ratio", Number(1.0))
		self.repeat_over = self.attrs.pop("repeat_over", String(""))
		self.start_at = self.attrs.pop("start_at", Number(0))
		self.padding = self.attrs.pop("padding", Number(0))
		
		
	def apply (self, generator, data={}):
		macrolist = data.get(str(self.repeat_over), {})
	
		output = generator.generateGroup(self, macros=data)
		
		if not isinstance(macrolist, list):
			if isinstance(macrolist, DataType):
				macrolist = [ {"N" : x} for x in range(int(self.start_at), int(self.start_at) + int(macrolist)) ]
			else:
				macrolist = [ {"N" : x} for x in range(int(self.start_at), int(self.start_at) + int(macrolist)) ]
	
		num_items = len(macrolist)
		
		cols = round(math.sqrt(num_items * float(self.ratio)))
		rows = round(math.sqrt(num_items / float(self.ratio)))
		
		index = 0
		index_x = 0
		index_y = 0
		
		for macroset in macrolist:
			child_macros = copy.deepcopy(data)
			child_macros.update(macroset)
			child_macros.update({"__index__" : index})
			child_macros.update({"__col__" : index_x})
			child_macros.update({"__row__" : index_y})
			
			element = generator.generateAnonymousGroup()
			
			for childnode in self.children:
				child_macros.update({
					"__parentx__" : output["geometry"]["x"],
					"__parenty__" : output["geometry"]["y"],
					"__parentwidth__" : output["geometry"]["width"],
					"__parentheight__" : output["geometry"]["height"]})
					
				element.place(childnode.apply(generator, data=child_macros))
			
			pos_x = index_x * (element["geometry"]["width"] + int(self.padding))
			pos_y = index_y * (element["geometry"]["height"] + int(self.padding))
				
			element.position(pos_x, pos_y)
			
			index += 1
			index_x += 1
			
			if index_x >= cols:
				index_x = 0
				index_y += 1
		
			output.place(element)
			
		return output

		
class FlowNode(GroupNode):
	def __init__(self, layout={}, flow="vertical"):
		super(FlowNode, self).__init__("caFrame", layout=layout)
	
		self.padding = self.attrs.pop("padding", Number(0))
		self.flow = flow
		
		
	def apply (self, generator, data={}):		
		output = generator.generateGroup(self, macros=data)
		
		child_macros = copy.deepcopy(data)
		
		first = 0
		
		for childnode in self.children:			
			child_macros.update({
				"__parentx__" : output["geometry"]["x"],
				"__parenty__" : output["geometry"]["y"],
				"__parentwidth__" : output["geometry"]["width"],
				"__parentheight__" : output["geometry"]["height"]})
			
			element = childnode.apply(generator, data=child_macros)

			if self.flow == "vertical":
				element.position(x=None, y=output["geometry"]["height"] + (first*int(self.padding)))
				
			elif self.flow == "horizontal":
				element.position(x=output["geometry"]["width"] + (first * int(self.padding)), y=None)
			
			output.place(element)
			first = 1
			
		return output
		
		
class RepeatNode(GroupNode):
	def __init__(self, layout={}, flow="vertical"):
		super(RepeatNode, self).__init__("caFrame", layout=layout)
	
		self.repeat_over = self.attrs.pop("repeat_over", String(""))
		self.start_at = self.attrs.pop("start_at", Number(0))
		self.padding = self.attrs.pop("padding", Number(0))
		self.flow = flow
	
		
	def apply (self, generator, data={}):		
		macrolist = data.get(str(self.repeat_over), None)
		
		output = generator.generateGroup(self, macros=data)
		
		index = 0
		
		if not isinstance(macrolist, list):
			if isinstance(macrolist, DataType):
				macrolist = [ {"N" : x} for x in range(int(self.start_at), int(self.start_at) + int(macrolist)) ]
			else:
				macrolist = [ {"N" : x} for x in range(int(self.start_at), int(self.start_at) + int(macrolist)) ]
		
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
						
				line.place(childnode.apply(generator, data=child_macros))
							
			if self.flow == "vertical":
				line.position(x=None, y=(index * (line["geometry"]["height"] + int(self.padding))))
				
			elif self.flow == "horizontal":
				line.position(x=(index * (line["geometry"]["width"] + int(self.padding))), y=None)
			
			output.place(line)
			index += 1
			
		return output


class ConditionalNode(GroupNode):
	def __init__(self, layout={}):
		super(ConditionalNode, self).__init__("caFrame", layout=layout)
		
		self.condition = self.attrs.get("condition", String(""))
		
	def apply(self, generator, data={}):
		output = generator.generateAnonymousGroup()
		output.position(self["geometry"]["x"], self["geometry"]["y"])
		
		conditional = data.get(str(self.condition), None)
		
		if bool(conditional):
			child_macros = copy.deepcopy(data)
			
			for childnode in self.children:
				child_macros.update({
					"__parentx__" : output["geometry"]["x"],
					"__parenty__" : output["geometry"]["y"],
					"__parentwidth__" : output["geometry"]["width"],
					"__parentheight__" : output["geometry"]["height"]})
				
				output.place(childnode.apply(generator, data=data))
		
		return output

		
class SpacerNode(Node):
	def __init__(self, layout={}):
		super(SpacerNode, self).__init__("Spacer", layout=layout)
	
	def apply(self, generator, data={}):
		output = generator.generateAnonymousGroup()
		output["geometry"] = self["geometry"]
		
		return output
		
		
class StretchNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None):
		super(StretchNode, self).__init__("Stretch", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def apply (self, generator, data={}):
		self.subnode["geometry"]["x"] = self.subnode["geometry"]["x"] + self["geometry"]["x"]
		self.subnode["geometry"]["y"] = self.subnode["geometry"]["y"] + self["geometry"]["y"]
		
		if self.flow == "vertical":
			self.subnode["geometry"]["height"] = data["__parentheight__"]
		elif self.flow == "horizontal":
			self.subnode["geometry"]["width"] = data["__parentwidth__"]
		
		return self.subnode.apply(generator, data=data)

		
class CenterNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None):
		super(CenterNode, self).__init__("Center", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def apply (self, generator, data={}):
		applied_node = self.subnode.apply(generator, data=data)
			
		if self.flow == "vertical":
			applied_node.position(applied_node["geometry"]["x"] + self["geometry"]["x"], int(data["__parentheight__"] / 2) - int(applied_node["geometry"]["height"] / 2))
		elif self.flow == "horizontal":
			applied_node.position(int(data["__parentwidth__"] / 2) - int(applied_node["geometry"]["width"] / 2), applied_node["geometry"]["y"] + self["geometry"]["y"])
					
		return applied_node	

		
class RelatedDisplayNode(Node):
	def __init__(self, name=None, layout={}):
		self.links = layout.pop("links", [])
	
		super(RelatedDisplayNode, self).__init__("RelatedDisplay", name=name, layout=layout)
	
		if isinstance(self.links, dict):
			temp = []
			
			for key, val in self.items():
				val["label"] = key
				temp.append(val)
				
			self.links = temp
			
	def apply(self, generator, data={}):
		return generator.generateRelatedDisplay(self, data)
