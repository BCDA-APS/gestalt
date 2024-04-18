import yaml
import copy
import math
import string

from gestalt.Datasheet import *
from gestalt.Type import *

import tkinter as tk
import tkinter.font as tkfont


class Node(object):
	def __init__(self, classname, name=None, node=None, layout={}):
		self.classname = classname
		self.name = name
		
		if node:
			self.name = node.name
			self.properties = copy.deepcopy(node.properties)
		else:
			self.properties = {}
			self.properties["attrs"] = {}
			self.properties["internal"]  = {}
		
			if layout is not None:
				for key, val in layout.items():
					self.setProperty(key, val)
		
			
		self.setDefault(Rect, "geometry", "0x0x0x0")
	
		
	def setDefault(self, datatype, key, default, internal=False):
		which = "internal" if internal else "attrs"
		self.properties[which][key] = datatype(self.properties[which].pop(key, default))
			
	def link(self, newkey, oldkey, internal=False):
		which = "internal" if internal else "attrs"
		self.properties[which][newkey] = self.properties[which].pop(oldkey)
		
	def pop(self, key, default=None, internal=False):
		which = "internal" if internal else "attrs"
		return self.properties[which].pop(key, default)
		
	def makeInternal(self, datatype, key, default=None):
		self.properties["internal"][key] = datatype(self.properties["attrs"].pop(key, default))
		
	def updateProperties(self, macros={}):
		for attr in self.properties["internal"].values():
			attr.apply(macros)
		
		for attr in self.properties["attrs"].values():
			attr.apply(macros)
			
	def setProperty(self, key, input, internal=False):
		which = "internal" if internal else "attrs"
		
		to_assign = None
		
		if isinstance(input, bool):
			to_assign = Bool(input)
		elif isinstance(input, int):
			to_assign = Number(input)
		elif isinstance(input, float):
			to_assign = Double(input)
		elif isinstance(input, str):
			to_assign = String(input)
		else:
			to_assign = copy.deepcopy(input)
							
		self.properties[which][key] = to_assign
	
		
	def setProperties(self, layout={"internal" : {}, "attrs" : {}}):	
		for key, val in layout["internal"].items():
			self.setProperty(key, val, internal=True)
			
		for key, val in layout["attrs"].items():
			self.setProperty(key, val)
	
		
	def getProperty(self, key, internal=False):
		which = "internal" if internal else "attrs"
		return self.properties[which][key]
		
		
	def __setitem__(self, key, data):
		self.setProperty(key, data)	
		
		
	def __getitem__(self, key):
		return self.getProperty(key)
		
	def __contains__(self, key):
		return key in self.properties["attrs"]
		
		
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

		if out_x is not None:
			self["geometry"]["x"] = out_x
		
		if out_y is not None:
			self["geometry"]["y"] = out_y
				
		return self

		
	def apply (self, generator, data={}):		
		gen_func = getattr(generator, "generate" + self.classname, None)
		
		if gen_func:
			return gen_func(self, macros=data)
		else:
			return generator.generateWidget(self, macros=data)
		
		
		
class GroupNode(Node):
	def __init__(self, classname, name=None, node=None, layout={}):	
		super(GroupNode, self).__init__(classname, name=name, node=node, layout=layout)
		
		self.children = []
		
		#if node and hasattr(node, "children"):
			#self.children = copy.deepcopy(node.children)
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
		
					
	def append(self, child, keep_original=False):					
		if not keep_original:
			self.children.append(copy.deepcopy(child))
		else:
			self.children.append(child)
		
		
	def place(self, child, x=None, y=None, keep_original=False):
		self.append(child, keep_original=keep_original)
		
		child_node = self.children[-1]
		
		margins = self.getProperty("margins", internal=True).val()
		child_geom = child_node["geometry"].val()
		my_geom = self["geometry"].val()
		
		if x:
			child_node["geometry"]["x"] = x + int(margins["x"])
		else:
			child_node["geometry"]["x"] = int(child_geom["x"]) + int(margins["x"])
			
		if y:
			child_node["geometry"]["y"] = y + int(margins["y"])
		else:
			child_node["geometry"]["y"] = int(child_geom["y"]) + int(margins["y"])
		
			
		# Don't use child_geom for x/y as the value may have updated
		right_edge  = int(child_node["geometry"]["x"]) + int(child_geom["width"]) + int(margins["width"])
		bottom_edge = int(child_node["geometry"]["y"]) + int(child_geom["height"]) + int(margins["height"])
		
		if right_edge > int(my_geom["width"]):
			self["geometry"]["width"] = right_edge
			
		if bottom_edge > int(my_geom["height"]):
			self["geometry"]["height"] = bottom_edge
		
	
	def apply (self, generator, data={}):
		output = generator.generateGroup(self, macros=data)
		margins = self.getProperty("margins", internal=True).val()
		
		child_macros = copy.deepcopy(data)
		
		for child in self.children:
			geom = output["geometry"].val()
			
			child_macros.update({
				"__parentx__" : int(geom["x"]),
				"__parenty__" : int(geom["y"]),
				"__parentwidth__" : int(geom["width"]),
				"__parentheight__" : int(geom["height"])})
						
			output.place(child.apply(generator, data=child_macros))
			
		return output

class TabbedGroupNode(GroupNode):
	def __init__(self, name=None, layout={}):		
		super(TabbedGroupNode, self).__init__("TabbedGroup", name=name, layout=layout)
		
		self.setDefault(Color,  "foreground",     "$000000")
		self.setDefault(Color,  "background",     "$00000000")
		self.setDefault(Color,  "tab-color",      "$D2D2D2")
		self.setDefault(Color,  "selected",       "$A8A8A8")
		self.setDefault(Color,  "border-color",   "$000000")
		self.setDefault(Number, "border-width",   0)
		self.setDefault(Number, "padding",        5)
		self.setDefault(Number, "inset",          0)
		self.setDefault(Number, "offset",         0)
		self.setDefault(Font,   "font",           "-Liberation Sans - Regular - 12")
		
	def apply(self, generator, data={}):
		output = generator.generateTabbedGroup(self, macros=data)
		
		tk_root = tk.Tk()
		tk_root.withdraw()
		
		the_font = output["font"]
		
		tk_font = tkfont.Font(family=the_font["family"], size=int(the_font["size"]))
		
		tab_bar_height = tk_font.metrics("linespace") + 4 + int(output["offset"])
		
		tk_root.destroy()
		
		border_size = int(output["border-width"])
		
		if output["border-color"]["alpha"] == 0:
			border_size = 0
		
		for childnode in self.children:
			child_macros = copy.deepcopy(data)
			
			geom = output["geometry"].val()
			
			childnode["geometry"]["width"] = int(geom["width"]) - 2 * border_size
			childnode["geometry"]["height"] = int(geom["height"]) - tab_bar_height - 2 * border_size
			
			output.place(childnode.apply(generator, data=child_macros))
			
		return output
		
		
class GridNode(GroupNode):
	def __init__(self, name=None, layout={}):
		super(GridNode, self).__init__("caFrame", layout=layout)
	
		self.makeInternal(Double, "aspect-ratio", 1.0)
		self.makeInternal(String, "repeat-over", "")
		self.makeInternal(Number, "start-at", 0)
		self.makeInternal(Number, "padding", 0)
		self.makeInternal(Bool,   "horizontal", True)
		
		
	def apply (self, generator, data={}):
		output = generator.generateGroup(self, macros=data)
		
		repeat = output.getProperty("repeat-over", internal=True)
		
		macrolist = data.get(str(repeat), None)
		start_at = output.getProperty("start-at", internal=True)
		ratio    = output.getProperty("aspect-ratio", internal=True)
		padding  = output.getProperty("padding", internal=True)
		margins  = output.getProperty("margins", internal=True).val()
				
		
		if not macrolist:
			macrolist = [ {"N" : x} for x in range(int(start_at), int(start_at) + int(repeat)) ]
		if not isinstance(macrolist, list):
			macrolist = [ {"N" : x} for x in range(int(start_at), int(start_at) + int(macrolist)) ]
				
		num_items = len(macrolist)
		
		cols = round(math.sqrt(num_items * float(ratio)))
		rows = round(math.sqrt(num_items / float(ratio)))
		
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
				geom = output["geometry"].val()
			
				child_macros.update({
					"__parentx__" : int(geom["x"]),
					"__parenty__" : int(geom["y"]),
					"__parentwidth__" : int(geom["width"]) - int(margins["x"]) - int(margins["width"]),
					"__parentheight__" : int(geom["height"]) - int(margins["y"]) - int(margins["height"])})
					
				element.place(childnode.apply(generator, data=child_macros))
			
			pos_x = index_x * (element["geometry"]["width"] + int(padding))
			pos_y = index_y * (element["geometry"]["height"] + int(padding))
			
			element.position(pos_x, pos_y)
			
			index += 1
			
			if output.getProperty("horizontal", internal=True):
				index_x += 1
				
				if index_x >= cols:
					index_x = 0
					index_y += 1
					
			else:
				index_y += 1
				
				if index_y >= rows:
					index_y = 0
					index_x += 1
			
			output.place(element)
			
		return output

		
class FlowNode(GroupNode):
	def __init__(self, layout={}, flow="vertical"):
		super(FlowNode, self).__init__("caFrame", layout=layout)
	
		self.makeInternal(Number, "padding", 0)
		self.flow = flow
		
		
	def apply (self, generator, data={}):
		output = generator.generateGroup(self, macros=data)
		padding = output.getProperty("padding", internal=True)
		margins = output.getProperty("margins", internal=True).val()
		
		child_macros = copy.deepcopy(data)
		
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
			
			if self.flow == "vertical":
				element.position(x=None, y=position + (first*int(padding)))
				position = int(element["geometry"]["y"]) + int(element["geometry"]["height"])
				
			elif self.flow == "horizontal":
				element.position(x=position + (first * int(padding)), y=None)
				position = int(element["geometry"]["x"]) + int(element["geometry"]["width"])
			
			output.place(element)
			
			first = 1
			
		return output
		
		
class RepeatNode(GroupNode):
	def __init__(self, layout={}, flow="vertical"):
		super(RepeatNode, self).__init__("caFrame", layout=layout)
	
		self.makeInternal(String, "repeat-over", "")
		self.makeInternal(Number, "start-at", 0)
		self.makeInternal(Number, "padding", 0)
		self.flow = flow
	
		
	def apply (self, generator, data={}):		
		output = generator.generateGroup(self, macros=data)
		
		repeat = output.getProperty("repeat-over", internal=True)
		
		macrolist = data.get(str(repeat), None)
		start_at = output.getProperty("start-at", internal=True)
		padding  = output.getProperty("padding", internal=True)
		
		index = 0
		
		if not macrolist:
			macrolist = [ {"N" : x} for x in range(int(start_at), int(start_at) + int(repeat)) ]
		elif not isinstance(macrolist, list):
			macrolist = [ {"N" : x} for x in range(int(start_at), int(start_at) + int(macrolist)) ]
					
		for macroset in macrolist:
			child_macros = copy.deepcopy(data)
			child_macros.update(macroset)
			child_macros.update({"__index__" : index})
			
			line = generator.generateAnonymousGroup()
			
			for childnode in self.children:				
				geom = output["geometry"].val()
			
				child_macros.update({
					"__parentx__" : int(geom["x"]),
					"__parenty__" : int(geom["y"]),
					"__parentwidth__" : int(geom["width"]),
					"__parentheight__" : int(geom["height"])})
				
				line.place(childnode.apply(generator, data=child_macros))
							
			if self.flow == "vertical":
				line.position(x=None, y=(index * (line["geometry"]["height"] + int(padding))))
				
			elif self.flow == "horizontal":
				line.position(x=(index * (line["geometry"]["width"] + int(padding))), y=None)
			
			output.place(line)
			index += 1
			
		return output


class ConditionalNode(GroupNode):
	def __init__(self, layout={}):
		super(ConditionalNode, self).__init__("caFrame", layout=layout)
		
		self.makeInternal(String, "condition", "")
		
	def apply(self, generator, data={}):
		output = generator.generateAnonymousGroup()
		output.position(self["geometry"]["x"], self["geometry"]["y"])

		condition = self.getProperty("condition", internal=True)
		condition.apply(data)
		conditional = data.get(str(condition), None)
		
		if bool(conditional):
			child_macros = copy.deepcopy(data)
			
			for childnode in self.children:
				geom = output["geometry"].val()
			
				child_macros.update({
					"__parentx__" : int(geom["x"]),
					"__parenty__" : int(geom["y"]),
					"__parentwidth__" : int(geom["width"]),
					"__parentheight__" : int(geom["height"])})
				
				output.place(childnode.apply(generator, data=child_macros))
		
		return output
		
		
class ApplyNode(Node):
	def __init__(self, layout={}, defaults={}, macros={}, subnode=None):
		super(ApplyNode, self).__init__("Apply", layout=layout)
		
		self.defaults = defaults
		self.macros = macros
		self.subnode = subnode
		
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
		
				
		return self.subnode.apply(generator, data=child_macros)

		
class SpacerNode(Node):
	def __init__(self, layout={}):
		super(SpacerNode, self).__init__("Spacer", layout=layout)
	
	def apply(self, generator, data={}):
		output = generator.generateAnonymousGroup()
		output["geometry"] = self["geometry"]
		output["geometry"].apply(data)
		
		return output
		
		
class StretchNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None):
		super(StretchNode, self).__init__("Stretch", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def apply (self, generator, data={}):
		applied_node = copy.deepcopy(self.subnode)
		
		if self.flow == "vertical" or self.flow == "all":
			applied_node["geometry"]["height"] = data["__parentheight__"]
		if self.flow == "horizontal" or self.flow=="all":
			applied_node["geometry"]["width"] = data["__parentwidth__"]
			
		applied_node = applied_node.apply(generator, data=data)
			
		applied_node["geometry"]["x"] = applied_node["geometry"]["x"] + self["geometry"]["x"]
		applied_node["geometry"]["y"] = applied_node["geometry"]["y"] + self["geometry"]["y"]
			
		return applied_node

		
class CenterNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None):
		super(CenterNode, self).__init__("Center", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def apply (self, generator, data={}):
		applied_node = self.subnode.apply(generator, data=data)
			
		if self.flow == "vertical":
			applied_node.position(applied_node["geometry"]["x"] + self["geometry"]["x"], int(int(data["__parentheight__"]) / 2) - int(int(applied_node["geometry"]["height"]) / 2))
		elif self.flow == "horizontal":
			applied_node.position(int(int(data["__parentwidth__"]) / 2) - int(int(applied_node["geometry"]["width"]) / 2), applied_node["geometry"]["y"] + self["geometry"]["y"])
		elif self.flow == "all":
			applied_node.position(int(int(data["__parentwidth__"]) / 2) - int(int(applied_node["geometry"]["width"]) / 2), int(int(data["__parentheight__"]) / 2) - int(int(applied_node["geometry"]["height"]) / 2))
					
		return applied_node	

		
class RelatedDisplayNode(Node):
	def __init__(self, name=None, layout={}):
		self.links = layout.pop("links", [])
	
		super(RelatedDisplayNode, self).__init__("RelatedDisplay", name=name, layout=layout)
		
		self.setDefault(String, "text", "")
		self.setDefault(Font,  "font", "-Liberation Sans - Regular - 12")
		self.setDefault(Color, "foreground", "$000000")
		self.setDefault(Color, "background", "$57CAE4")
	
		if isinstance(self.links, dict):
			temp = []
			
			for key, val in self.items():
				val["label"] = key
				temp.append(val)
				
			self.links = temp

			
class MessageButtonNode(Node):
	def __init__(self, name=None, layout={}):
		super(MessageButtonNode, self).__init__("MessageButton", name=name, layout=layout)		
		self.setDefault(String, "text",  "")
		self.setDefault(String, "pv",    "")
		self.setDefault(String, "value", "")
		self.setDefault(Font,  "font", "-Liberation Sans - Regular - 12")
		self.setDefault(Color,  "foreground", "$000000")
		self.setDefault(Color,  "background", "$57CAE4")
	

class TextNode(Node):
	def __init__(self, name=None, layout={}):
		super(TextNode, self).__init__("Text", name=name, layout=layout)
		
		self.setDefault(Color,     "foreground",   "$000000")
		self.setDefault(Color,     "background",   "$00000000")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",    "CenterLeft")

class TextEntryNode(Node):
	def __init__(self, name=None, layout={}):
		super(TextEntryNode, self).__init__("TextEntry", name=name, layout=layout)
	
		self.setDefault(String,    "pv",         "")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",  "CenterLeft")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Color,     "foreground", "$000000")

class TextMonitorNode(Node):
	def __init__(self, name=None, layout={}):
		super(TextMonitorNode, self).__init__("TextMonitor", name=name, layout=layout)
	
		self.setDefault(String,    "pv",           "")
		self.setDefault(Color,     "foreground",   "$000000")
		self.setDefault(Color,     "background",   "$00000000")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",    "CenterLeft")

class MenuNode(Node):
	def __init__(self, name=None, layout={}):
		super(MenuNode, self).__init__("Menu", name=name, layout=layout)
	
		self.setDefault(String, "pv", "")
	
class ChoiceButtonNode(Node):
	def __init__(self, name=None, layout={}):
		super(ChoiceButtonNode, self).__init__("ChoiceButton", name=name, layout=layout)
	
		self.setDefault(String, "pv",         "")
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(Color,  "background", "$C8C8C8")
		self.setDefault(Color,  "selected",   self["background"])
	
class LEDNode(Node):
	def __init__(self, name=None, layout={}):
		super(LEDNode, self).__init__("LED", name=name, layout=layout)
	
		self.setDefault(String, "pv",             "")
		self.setDefault(Bool,   "square",         False)
	
		self.setDefault(Color, "false-color",     "$3C643C")
		self.setDefault(Color, "true-color",      "$00FF00")
		self.setDefault(Color, "undefined-color", "$A0A0A4")
		self.setDefault(Color, "border-color",    "$000000")
	
		self.setDefault(Number, "false-value", 0)
		self.setDefault(Number, "true-value", 1)

	
class ByteMonitorNode(Node):
	def __init__(self, name=None, layout={}):
		super(ByteMonitorNode, self).__init__("ByteMonitor", name=name, layout=layout)
		
		self.setDefault(String,  "pv",          "")
		self.setDefault(Bool,    "horizontal",  True)
		self.setDefault(Number,  "start-bit",   0)
		self.setDefault(Number,  "bits",        (32 - int(self["start-bit"])))
		self.setDefault(Color,   "off-color",   "$3C643C")
		self.setDefault(Color,   "on-color",    "$00FF00")
	

class RectangleNode(Node):
	def __init__(self, name=None, layout={}):
		super(RectangleNode, self).__init__("Rectangle", name=name, layout=layout)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
	
		
class EllipseNode(Node):
	def __init__(self, name=None, layout={}):
		super(EllipseNode, self).__init__("Ellipse", name=name, layout=layout)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
	

class ArcNode(Node):
	def __init__(self, name=None, layout={}):
		super(ArcNode, self).__init__("Arc", name=name, layout=layout)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(Number, "start-angle", 0)
		self.setDefault(Number, "span", 90)

		
class ImageNode(Node):
	def __init__(self, name=None, layout={}):
		super(ImageNode, self).__init__("Image", name=name, layout=layout)
		
		self.setDefault(String, "file", "")

		
class SliderNode(Node):
	def __init__(self, name=None, layout={}):
		super(SliderNode, self).__init__("Slider", name=name, layout=layout)
		
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(String, "pv",         "")
		

class ScaleNode(Node):
	def __init__(self, name=None, layout={}):
		super(ScaleNode, self).__init__("Scale", name=name, layout=layout)
		
		self.setDefault(String, "pv",          "")
		self.setDefault(Color,  "background",  "$C0C0C0")
		self.setDefault(Color,  "foreground",  "$0000FF")
		self.setDefault(Bool,   "horizontal",  False)

		
class ShellCommandNode(Node):
	def __init__(self, name=None, layout={}):
		self.commands = layout.pop("commands", [])
	
		super(ShellCommandNode, self).__init__("ShellCommand", name=name, layout=layout)
		
		self.setDefault(String, "text", "")
	
		if isinstance(self.commands, dict):
			temp = []
			
			for key, val in self.items():
				val["label"] = key
				temp.append(val)
				
			self.commands = temp
		

class PolygonNode(Node):
	def __init__(self, name=None, layout={}):
		self.points = layout.pop("points", [])
		
		super(PolygonNode, self).__init__("Polygon", name=name, layout=layout)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)

		
class PolylineNode(Node):
	def __init__(self, name=None, layout={}):
		self.points = layout.pop("points", [])
		
		super(PolylineNode, self).__init__("Polyline", name=name, layout=layout)
		
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		
		
