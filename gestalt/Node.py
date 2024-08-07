import yaml
import copy
import math
import pprint
import string

from gestalt.Generator import GestaltGenerator
from gestalt.Datasheet import *
from gestalt.Type import *

class Node(object):
	def __init__(self, classname, name=None, node=None, layout={}, loc=None):
		self.classname = classname
		self.name = name
		self.location = loc
		self.debug = False
		
		self.properties = {}
		self.properties["attrs"] = {}
		self.properties["internal"]  = {}
		
		self.tocopy = []
		
		if node:
			self.name = node.name
			self.location = node.location
			self.debug = node.debug
			
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
	
	def log(self, info):
		if self.debug:
			print(str(self.name) + ": " + info)
		
		
	def setDefault(self, datatype, key, default, internal=False):
		which = "internal" if internal else "attrs"
		self.properties[which][key] = datatype(self.properties[which].pop(key, default))
			
	def link(self, newkey, oldkey, conversion=None):
		which = "attrs"
		
		if oldkey in self.properties["internal"]:
			which = "internal"
		
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
		
	def makeInternal(self, datatype, key, default=None):
		if key not in self.properties["internal"]:
			self.properties["internal"][key] = datatype(self.properties["attrs"].pop(key, default))
		elif key in self.properties["attrs"]:
			self.properties["internal"][key] = datatype(self.properties["attrs"].pop(key))
		
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

		which = "attrs"
			
		if key in self.properties["internal"] or internal:
			which = "internal"
			
		if isinstance(to_assign, DataType):
			self.log("Setting Property " + key + " from " + str(self.properties[which].get(key)) + " to " + str(to_assign.value))
		else:
			self.log("Setting Property " + key + " from " + str(self.properties[which].get(key)) + " to " + pprint.pformat(to_assign))
			
		self.properties[which][key] = to_assign
	
		
	def setProperties(self, layout={"internal" : {}, "attrs" : {}}):
		for key, val in layout["internal"].items():
			self.setProperty(key, val, internal=True)
			
		for key, val in layout["attrs"].items():
			self.setProperty(key, val)
	
		
	def getProperty(self, key, internal=False):
		if key not in self.properties["attrs"] or internal:
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

		
	def apply (self, generator, data={}):		
		gen_func = getattr(generator, "generate" + self.classname, None)
				
		if gen_func:
			self.log("Generating " + self.classname)
			return gen_func(self, macros=data)
		else:
			self.log("Generating generic widget")
			return generator.generateWidget(self, macros=data)
			
	def __deepcopy__(self, memo):
		cls = self.__class__
		output = cls.__new__(cls)
		
		output.classname = self.classname
		output.name = self.name
		output.location = self.location
		output.debug = self.debug
		
		output.properties = {}
		output.properties["attrs"] = copy.copy(self.properties["attrs"])
		output.properties["internal"] = copy.copy(self.properties["internal"])
		
		output.tocopy = copy.copy(self.tocopy)

		for attr in self.tocopy:
			setattr(output, attr, copy.deepcopy(getattr(self, attr), memo))
		
		memo[id(self)] = output
		
		return output
		
		
		
class GroupNode(Node):
	def __init__(self, classname, name=None, node=None, layout={}, loc=None):	
		super(GroupNode, self).__init__(classname, name=name, node=node, layout=layout, loc=loc)
		
		self.children = []
		
		if not node:
			initial = self.pop("children", [])
		
			if isinstance(initial, dict):
				for childname, child in initial.items():
					child.name = childname
					self.append(child)
			
			elif isinstance(initial, list):
				for child in initial:
					self.append(child)
		
			self.makeInternal(Rect, "margins", "0x0x0x0")
				
		self.setDefault(Rect, "margins", "0x0x0x0", internal=True)
		self.setDefault(Number, "border-width",   0)
		
					
	def append(self, child, keep_original=False):
		self.log("Adding child node " + child.__repr__())
		
		if not keep_original:
			self.children.append(copy.deepcopy(child))
		else:
			self.children.append(child)
		
	def __iter__(self):
		return self.children.__iter__()
		
	def place(self, child, x=None, y=None, keep_original=False):
		self.append(child, keep_original=keep_original)
		
		child_node = self.children[-1]
		
		margins = self["margins"].val()
		
		child_geom = child_node["geometry"].val()
		my_geom = self["geometry"].val()
		border = int(self["border-width"])
		
		if x:
			child_node["geometry"]["x"] = x + int(margins["x"]) + border
		else:
			child_node["geometry"]["x"] = int(child_geom["x"]) + int(margins["x"]) + border
			
		if y:
			child_node["geometry"]["y"] = y + int(margins["y"]) + border
		else:
			child_node["geometry"]["y"] = int(child_geom["y"]) + int(margins["y"]) + border
		
			
		# Don't use child_geom for x/y as the value may have updated
		right_edge  = int(child_node["geometry"]["x"]) + int(child_geom["width"]) + int(margins["width"])
		bottom_edge = int(child_node["geometry"]["y"]) + int(child_geom["height"]) + int(margins["height"])
		
		if right_edge > int(my_geom["width"]):
			self.log("Resizing width to " + str(right_edge))
			self["geometry"]["width"] = right_edge
			
		if bottom_edge > int(my_geom["height"]):
			self.log("Resizing height to " + str(bottom_edge))
			self["geometry"]["height"] = bottom_edge
	
	def apply (self, generator, data={}):
		self.log("Generating group node")
		output = generator.generateGroup(self, macros=data)

		margins = self["margins"].val()
		border = int(self["border-width"])
		
		child_macros = copy.copy(data)
		
		for child in self:
			geom = output["geometry"].val()
			
			child_macros.update({
				"__parentx__" : int(geom["x"]),
				"__parenty__" : int(geom["y"]),
				"__parentwidth__" : int(geom["width"]) - int(margins["x"]) - int(margins["width"]) - 2 * border,
				"__parentheight__" : int(geom["height"]) - int(margins["y"]) - int(margins["height"]) - 2 * border})
			
			output.place(child.apply(generator, data=child_macros))
			
		return output
		
	def __deepcopy__(self, memo):
		output = super().__deepcopy__(memo)
		
		output.children = copy.copy(self.children)
		
		return output
		
class TabbedGroupNode(GroupNode):
	def __init__(self, name=None, layout={}, loc=None):		
		super(TabbedGroupNode, self).__init__("TabbedGroup", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "foreground",     "$000000")
		self.setDefault(Color,  "background",     "$00000000")
		self.setDefault(Color,  "tab-color",      "$D2D2D2")
		self.setDefault(Color,  "selected",       "$A8A8A8")
		self.setDefault(Color,  "border-color",   "$000000")
		self.setDefault(String, "border-style",   "Solid")
		self.setDefault(Number, "border-width",   0)
		self.setDefault(Number, "padding",        5)
		self.setDefault(Number, "inset",          0)
		self.setDefault(Number, "offset",         0)
		self.setDefault(Font,   "font",           "-Liberation Sans - Regular - 12")
		
	def apply(self, generator, data={}):
		self.log("Generating Tabbed Group")
		output = generator.generateTabbedGroup(self, macros=data)
		
		the_font = output["font"]
		
		tab_bar_height = GestaltGenerator.get_font_height(the_font["family"], int(the_font["size"]))
		tab_bar_height += 4 + int(output["offset"])
		
		border_size = int(output["border-width"])
		
		if output["border-color"]["alpha"] == 0:
			border_size = 0
		
		for childnode in self.children:
			child_macros = copy.copy(data)
			
			geom = output["geometry"].val()
			
			childnode["geometry"]["width"] = int(geom["width"]) - 2 * border_size
			childnode["geometry"]["height"] = int(geom["height"]) - tab_bar_height - 2 * border_size
			
			output.place(childnode.apply(generator, data=child_macros))
			
		return output


class LayoutNode(GroupNode):
	def __init__(self, name=None, layout={}, loc=None):
		super(LayoutNode, self).__init__("Layout", name=name, layout=layout, loc=loc)
		
		self.makeInternal(String, "repeat-over",  "")
		self.makeInternal(String, "variable",     "N")
		self.makeInternal(Number, "start-at",     0)
		self.makeInternal(Number, "padding",      0)
		
		self.makeInternal(Number, "index",     0)
		self.makeInternal(Number, "num-items", 0)
		self.makeInternal(Number, "last_x",    0)
		self.makeInternal(Number, "last_y",    0)
		
	def updateMacros(self, child_macros):
		child_macros.update({"__index__"   : self["index"].val()})
		
	def positionNext(self, output, line):
		pass
		
	def apply(self, generator, data={}):
		output = generator.generateGroup(self, macros=data)
		
		repeat   = output["repeat-over"]
		start_at = output["start-at"]
		
		index_var = output["index-variable"]
		value_var = output["value-variable"]
		
		#repeat.apply(data)
		
		macrolist = data.get(str(repeat))
		
		try:
			if not macrolist:
				macrolist = range(int(start_at), int(start_at) + int(repeat))
			elif not isinstance(macrolist, list):
				macrolist = range(int(start_at), int(start_at) + int(macrolist))
		except:
			macrolist = List(repeat).val()
					
		self["index"] = 0
		self["num-items"] = len(macrolist)
		self["last-x"] = 0
		self["last-y"] = 0
		
		if macrolist:
			for item in macrolist:
				geom = output["geometry"].val()
				
				child_macros = copy.copy(data)
				
				if isinstance(item, dict):
					child_macros.update(item)
				else:
					child_macros.update({str(value_var) : item})
					
				child_macros.update({
						"__parentx__" : int(geom["x"]),
						"__parenty__" : int(geom["y"]),
						"__parentwidth__" : int(geom["width"]),
						"__parentheight__" : int(geom["height"])})
						
				self.updateMacros(child_macros)
				
				line = generator.generateAnonymousGroup()
				
				for childnode in self.children:
					line.place(childnode.apply(generator, data=child_macros))
								
				self.positionNext(line)
				output.place(line)
				self["index"] = self["index"].val() + 1
			
		return output
		
		
class RepeatNode(LayoutNode):
	def __init__(self, name=None, layout={}, flow="vertical", loc=None):
		super(RepeatNode, self).__init__(name=name, layout=layout, loc=loc)
	
		self.setProperty("flow", flow, internal=True)
		
	def positionNext(self, line):		
		if self["flow"].val() == "vertical":
			line.position(x=None, y= self["last-y"].val())
			self["last-y"] = self["last-y"].val() + line["geometry"]["height"] + int(self["padding"])
			
		elif self["flow"].val() == "horizontal":
			line.position(x=self["last-x"].val(), y=None)
			self["last-x"] = self["last-x"].val() + line["geometry"]["width"] + int(self["padding"])
		
class GridNode(LayoutNode):
	def __init__(self, name=None, layout={}, loc=None):
		super(GridNode, self).__init__(name=name, layout=layout, loc=loc)
	
		self.makeInternal(Double, "aspect-ratio", 1.0)
		self.makeInternal(Bool,   "horizontal", True)
		
		self.makeInternal(Number, "index-x", 0)
		self.makeInternal(Number, "index-y", 0)
		
	def updateMacros(self, child_macros):
		super().updateMacros(child_macros)
		
		child_macros.update({
			"__col__" : self["index-x"].val(),
			"__row__" : self["index-y"].val()})

	def positionNext(self, line):
		ratio = self["aspect-ratio"].val()
		
		cols = round(math.sqrt(int(self["num-items"]) * float(ratio)))
		rows = round(math.sqrt(int(self["num-items"]) / float(ratio)))
		
		pos_x = int(self["index-x"]) * (line["geometry"]["width"] + int(self["padding"]))
		pos_y = int(self["index-y"]) * (line["geometry"]["height"] + int(self["padding"]))
		
		line.position(x=pos_x, y=pos_y)

		span, scale = "index-x", "index-y"
		
		if self["horizontal"]:
			self["index-x"] = self["index-x"].val() + 1
			
			if int(self["index-x"]) >= cols:
				self["index-x"] = 0
				self["index-y"] = self["index-y"].val() + 1
				
		else:
			self["index-y"] = self["index-y"].val() + 1
			
			if int(self["index-y"]) >= rows:
				self["index-y"] = 0
				self["index-x"] = self["index-x"].val() + 1
			
	def apply (self, generator, data={}):
		self["index-x"] = 0
		self["index-y"] = 0
		
		return super().apply(generator, data)
		
		
class FlowNode(GroupNode):
	def __init__(self, layout={}, flow="vertical", loc=None):
		super(FlowNode, self).__init__("caFrame", layout=layout, loc=loc)
	
		self.makeInternal(Number, "padding", 0)
		self.setProperty("flow", flow, internal=True)
		
		
	def apply (self, generator, data={}):
		output = generator.generateGroup(self, macros=data)
		padding = output["padding"]
		margins = output["margins"].val()
		flow    = output["flow"].val()
		
		child_macros = copy.copy(data)
		
		first = 0
		position = 0
		
		for childnode in self.children:
			geom = output["geometry"].val()
			
			child_macros.update({
				"__parentx__" : int(geom["x"]),
				"__parenty__" : int(geom["y"]),
				"__parentwidth__" : int(geom["width"]) - int(margins["x"]) - int(margins["width"]),
				"__parentheight__" : int(geom["height"]) - int(margins["y"]) - int(margins["height"])})
				
			element = childnode.apply(generator, data=child_macros)
			
			if flow == "vertical":
				element.position(x=None, y=position + (first*int(padding)))
				position = int(element["geometry"]["y"]) + int(element["geometry"]["height"])
				
			elif flow == "horizontal":
				element.position(x=position + (first * int(padding)), y=None)
				position = int(element["geometry"]["x"]) + int(element["geometry"]["width"])
			
			output.place(element)
			
			first = 1
			
		return output


class ConditionalNode(GroupNode):
	def __init__(self, layout={}, loc=None):
		super(ConditionalNode, self).__init__("caFrame", layout=layout, loc=loc)
		
		self.condition = self.pop("condition", "")
		
		self.tocopy.append("condition")
		
	def apply(self, generator, data={}):
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
				output.place(childnode.apply(generator, data=data))
		
		return output
		
		
class ApplyNode(Node):
	def __init__(self, layout={}, defaults={}, macros={}, subnode=None, loc=None):
		super(ApplyNode, self).__init__("Apply", layout=layout, loc=loc)
		
		self.defaults = defaults
		self.macros = macros
		self.subnode = subnode
		
		self.tocopy.append("subnode")
		self.tocopy.append("macros")
		self.tocopy.append("defaults")
		
	def apply(self, generator, data={}):
		child_macros = {}
		macro_list = {}
		
		macro_list.update(self.defaults)
		macro_list.update(data)
		macro_list.update(self.macros)
		
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
				to_assign.apply(data)
				
			child_macros.update({key : to_assign})
		
				
		if self.name:
			self.subnode.name = self.name
			
		return self.subnode.apply(generator, data=child_macros)

		
class SpacerNode(Node):
	def __init__(self, layout={}, loc=None):
		super(SpacerNode, self).__init__("Spacer", layout=layout, loc=loc)
	
	def apply(self, generator, data={}):
		output = generator.generateAnonymousGroup()
		output["geometry"] = self["geometry"]
		output["geometry"].apply(data)
		
		return output
		
		
class StretchNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None, loc=None):
		super(StretchNode, self).__init__("Stretch", name=name, layout=layout, loc=loc)
				
		self.setProperty("flow", flow, internal=True)
		
		self.subnode = subnode
		self.tocopy.append("subnode")
		
	def apply (self, generator, data={}):
		applied_node = copy.deepcopy(self.subnode)
		
		flow = self["flow"].val()
		
		if flow == "vertical" or flow == "all":
			applied_node["geometry"]["height"] = data["__parentheight__"]
		if flow == "horizontal" or flow=="all":
			applied_node["geometry"]["width"] = data["__parentwidth__"]
			
		if self.name:
			applied_node.name = self.name
			
		applied_node = applied_node.apply(generator, data=data)
			
		applied_node["geometry"]["x"] = applied_node["geometry"]["x"] + self["geometry"]["x"]
		applied_node["geometry"]["y"] = applied_node["geometry"]["y"] + self["geometry"]["y"]
			
		return applied_node

		
class CenterNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None, loc=None):
		super(CenterNode, self).__init__("Center", name=name, layout=layout, loc=loc)
		
		self.setProperty("flow", flow, internal=True)
		
		self.subnode = subnode
		self.tocopy.append("subnode")
		
	def apply (self, generator, data={}):
		if self.name:
			self.subnode.name = self.name
			
		applied_node = self.subnode.apply(generator, data=data)
		
		flow = self["flow"].val()
			
		if flow == "vertical":
			applied_node.position(x=applied_node["geometry"]["x"] + self["geometry"]["x"], y=int(int(data["__parentheight__"]) / 2) - int(int(applied_node["geometry"]["height"]) / 2))
		elif flow == "horizontal":
			applied_node.position(x=int(int(data["__parentwidth__"]) / 2) - int(int(applied_node["geometry"]["width"]) / 2), y=applied_node["geometry"]["y"] + self["geometry"]["y"])
		elif flow == "all":
			applied_node.position(x=int(int(data["__parentwidth__"]) / 2) - int(int(applied_node["geometry"]["width"]) / 2), y=int(int(data["__parentheight__"]) / 2) - int(int(applied_node["geometry"]["height"]) / 2))
					
		return applied_node	

class AnchorNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None, loc=None):
		super(AnchorNode, self).__init__("Anchor", name=name, layout=layout, loc=loc)
		
		self.setProperty("flow", flow, internal=True)
		
		self.subnode = subnode
		self.tocopy.append("subnode")
		
		
	def apply (self, generator, data={}):
		if self.name:
			self.subnode.name = self.name
			
		applied_node = self.subnode.apply(generator, data=data)
			
		flow = self["flow"].val()
		
		if flow == "vertical":
			applied_node.position(x=applied_node["geometry"]["x"] + self["geometry"]["x"], y=int(data["__parentheight__"]) - int(applied_node["geometry"]["height"]))
		elif flow == "horizontal":
			applied_node.position(x=int(data["__parentwidth__"]) - int(applied_node["geometry"]["width"]), y=applied_node["geometry"]["y"] + self["geometry"]["y"])
		elif flow == "all":
			applied_node.position(x=int(data["__parentwidth__"]) - int(applied_node["geometry"]["width"]), y=int(data["__parentheight__"]) - int(applied_node["geometry"]["height"]))
					
		return applied_node	
		
		
class RelatedDisplayNode(Node):
	def __init__(self, name=None, layout={}, loc=None):		
		self.links = layout.pop("links", [])
	
		super(RelatedDisplayNode, self).__init__("RelatedDisplay", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,    "text",       "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Alignment, "alignment",  "Center")
		
		self.tocopy.append("links")
	
		if isinstance(self.links, dict):
			temp = []
			
			for key, val in self.links.items():
				val["label"] = key
				temp.append(val)
				
			self.links = temp

			
class MessageButtonNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(MessageButtonNode, self).__init__("MessageButton", name=name, layout=layout, loc=loc)
		self.setDefault(String,    "text",       "")
		self.setDefault(String,    "pv",         "")
		self.setDefault(String,    "value",      "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Alignment, "alignment",  "Center")
	

class TextNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(TextNode, self).__init__("Text", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,     "foreground",   "$000000")
		self.setDefault(Color,     "background",   "$00000000")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",    "CenterLeft")

class TextEntryNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(TextEntryNode, self).__init__("TextEntry", name=name, layout=layout, loc=loc)
	
		self.setDefault(String,    "pv",         "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(String,    "format",     "Decimal")
		self.setDefault(Alignment, "alignment",  "CenterLeft")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Color,     "foreground", "$000000")

class TextMonitorNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(TextMonitorNode, self).__init__("TextMonitor", name=name, layout=layout, loc=loc)
	
		self.setDefault(String,    "pv",           "")
		self.setDefault(Color,     "foreground",   "$000000")
		self.setDefault(Color,     "background",   "$00000000")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(String,    "format",       "Decimal")
		self.setDefault(Alignment, "alignment",    "CenterLeft")

class MenuNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(MenuNode, self).__init__("Menu", name=name, layout=layout, loc=loc)
	
		self.setDefault(String, "pv", "")
	
class ChoiceButtonNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ChoiceButtonNode, self).__init__("ChoiceButton", name=name, layout=layout, loc=loc)
	
		self.setDefault(String, "pv",         "")
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(Color,  "background", "$C8C8C8")
		self.setDefault(Color,  "selected",   self["background"])
	
class LEDNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(LEDNode, self).__init__("LED", name=name, layout=layout, loc=loc)
	
		self.setDefault(String, "pv",             "")
		self.setDefault(Bool,   "square",         False)
	
		self.setDefault(Color, "false-color",     "$3C643C")
		self.setDefault(Color, "true-color",      "$00FF00")
		self.setDefault(Color, "undefined-color", "$A0A0A4")
		self.setDefault(Color, "border-color",    "$000000")
	
		self.setDefault(Number, "false-value", 0)
		self.setDefault(Number, "true-value", 1)

	
class ByteMonitorNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ByteMonitorNode, self).__init__("ByteMonitor", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,  "pv",          "")
		self.setDefault(Bool,    "horizontal",  True)
		self.setDefault(Number,  "start-bit",   0)
		self.setDefault(Number,  "bits",        (32 - int(self["start-bit"])))
		self.setDefault(Color,   "off-color",   "$3C643C")
		self.setDefault(Color,   "on-color",    "$00FF00")
	

class RectangleNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(RectangleNode, self).__init__("Rectangle", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
	
		
class EllipseNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(EllipseNode, self).__init__("Ellipse", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
	

class ArcNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ArcNode, self).__init__("Arc", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
		self.setDefault(Number, "start-angle", 0)
		self.setDefault(Number, "span", 90)

		
class ImageNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ImageNode, self).__init__("Image", name=name, layout=layout, loc=loc)
		
		self.setDefault(String, "file", "")

		
class SliderNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(SliderNode, self).__init__("Slider", name=name, layout=layout, loc=loc)
		
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(String, "pv",         "")
		

class ScaleNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		super(ScaleNode, self).__init__("Scale", name=name, layout=layout, loc=loc)
		
		self.setDefault(String, "pv",          "")
		self.setDefault(Color,  "background",  "$C0C0C0")
		self.setDefault(Color,  "foreground",  "$0000FF")
		self.setDefault(Bool,   "horizontal",  False)

		
class ShellCommandNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.commands = layout.pop("commands", [])
	
		super(ShellCommandNode, self).__init__("ShellCommand", name=name, layout=layout, loc=loc)
		
		self.setDefault(String, "text", "")
		self.setDefault(Font,  "font", "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment", "Center")
		
		self.tocopy.append("commands")
	
		if isinstance(self.commands, dict):
			temp = []
			
			for key, val in self.commands.items():
				val["label"] = key
				temp.append(val)
				
			self.commands = temp
		

class PolygonNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.points = layout.pop("points", [])
		
		super(PolygonNode, self).__init__("Polygon", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
		
		self.tocopy.append("points")

		
class PolylineNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.points = layout.pop("points", [])
		
		super(PolylineNode, self).__init__("Polyline", name=name, layout=layout, loc=loc)
		
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(String, "border-style", "Solid")
		
		self.tocopy.append("points")
		
		
