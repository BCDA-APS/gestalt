import yaml
import copy
import math
import string


from gestalt.Type import *


class Node(object):
	def __init__(self, classname, name=None, layout={}):
		self.classname = classname
		self.name = None
		self.attrs = {}
		
		if name is not None:
			self.name = name
		
		if layout is not None:
			Node.setProperties(self, layout)
			
		self.setDefault(Rect, "geometry", "0x0x0x0")
	
		
	def setDefault(self, datatype, key, default):
		self.attrs[key] = datatype(self.attrs.pop(key, default))
			
	def link(self, newkey, oldkey):
		self.attrs[newkey] = self.attrs.pop(oldkey)
		
	def pop(self, key, default=None):
		return self.attrs.pop(key, default)
		
	def updateProperties(self, macros={}):
		for attr in self.attrs.values():
			attr.apply(macros)
			
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
		elif isinstance(data, str):
			to_assign = String(data)
		else:
			to_assign = data
							
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
		
	def __contains__(self, key):
		return key in self.attrs
		
		
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
		self.updateProperties(macros=data)
		return generator.generateWidget(self, macros=data)
		
		
		
class GroupNode(Node):
	def __init__(self, classname, name=None, layout={}):
		initial = layout.pop("children", {})
	
		super(GroupNode, self).__init__(classname, name=name, layout=layout)
		
		self.margins = Rect(self.pop("margins", "0x0x0x0"))
	
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
		self.updateProperties(macros=data)
		
		output = generator.generateGroup(self, macros=data)
		output.margins = self.margins
		
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
	
		self.ratio = Double(self.pop("aspect-ratio", 1.0))
		self.repeat_over = String(self.pop("repeat-over", ""))
		self.start_at = Number(self.pop("start-at", 0))
		self.padding = Number(self.pop("padding", 0))
		self.horizontal = Bool(self.pop("horizontal", True))
		
		
	def apply (self, generator, data={}):
		self.updateProperties(macros=data)
		self.repeat_over.apply(data)
		macrolist = data.get(str(self.repeat_over), {})
	
		output = generator.generateGroup(self, macros=data)
		output.margins = self.margins
		
		if not isinstance(macrolist, list):
			if isinstance(macrolist, DataType):
				macrolist = [ {"N" : x} for x in range(int(self.start_at), int(self.start_at) + int(macrolist.val())) ]
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
			
			if self.horizontal:
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
	
		self.padding = Number(self.pop("padding", 0))
		self.flow = flow
		
		
	def apply (self, generator, data={}):
		self.updateProperties(macros=data)
		output = generator.generateGroup(self, macros=data)
		output.margins = self.margins
		
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
	
		self.repeat_over = String(self.pop("repeat-over", ""))
		self.start_at = Number(self.pop("start-at", 0))
		self.padding = Number(self.pop("padding", 0))
		self.flow = flow
	
		
	def apply (self, generator, data={}):
		self.updateProperties(macros=data)
		self.repeat_over.apply(data)
		macrolist = data.get(str(self.repeat_over), None)
		
		output = generator.generateGroup(self, macros=data)
		output.margins = self.margins
		
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
		
		self.condition = String(self.pop("condition", ""))
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		output = generator.generateAnonymousGroup()
		output.position(self["geometry"]["x"], self["geometry"]["y"])

		self.condition.apply(data)
		conditional = data.get(str(self.condition), None)
		
		if bool(conditional):
			child_macros = copy.deepcopy(data)
			
			for childnode in self.children:
				child_macros.update({
					"__parentx__" : output["geometry"]["x"],
					"__parenty__" : output["geometry"]["y"],
					"__parentwidth__" : output["geometry"]["width"],
					"__parentheight__" : output["geometry"]["height"]})
				
				output.place(childnode.apply(generator, data=child_macros))
		
		return output
		
		
class ApplyNode(GroupNode):
	def __init__(self, layout={}, macros={}, subnode=None):
		super(ApplyNode, self).__init__("Apply", layout=layout)
		
		self.macros = macros
		self.subnode = subnode
		
	def apply(self, generator, data={}):
		child_macros = copy.deepcopy(data)
		
		for key, val in self.macros.items():
			to_update = String(val)
			to_update.apply(data)
		
			child_macros.update({key : str(to_update)})
		
		return self.subnode.apply(generator, data=child_macros)

		
class SpacerNode(Node):
	def __init__(self, layout={}):
		super(SpacerNode, self).__init__("Spacer", layout=layout)
	
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		output = generator.generateAnonymousGroup()
		output["geometry"] = self["geometry"]
		
		return output
		
		
class StretchNode(Node):
	def __init__(self, name=None, layout={}, flow="vertical", subnode=None):
		super(StretchNode, self).__init__("Stretch", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def apply (self, generator, data={}):
		self.subnode.updateProperties(macros=data)
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
		
		self.setDefault(String, "text", "")
	
		if isinstance(self.links, dict):
			temp = []
			
			for key, val in self.items():
				val["label"] = key
				temp.append(val)
				
			self.links = temp
			
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateRelatedDisplay(self, data)

			
class MessageButtonNode(Node):
	def __init__(self, name=None, layout={}):
		super(MessageButtonNode, self).__init__("MessageButton", name=name, layout=layout)
	
		self.setDefault(String, "text",  "")
		self.setDefault(String, "pv",    "")
		self.setDefault(String, "value", "")
	
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateMessageButton(self, data)
	

class TextNode(Node):
	def __init__(self, name=None, layout={}):
		super(TextNode, self).__init__("Text", name=name, layout=layout)
		
		self.setDefault(Color,     "background",   "$00000000")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",    "CenterLeft")
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateText(self, data)

class TextEntryNode(Node):
	def __init__(self, name=None, layout={}):
		super(TextEntryNode, self).__init__("TextEntry", name=name, layout=layout)
	
		self.setDefault(String,    "pv",        "")
		self.setDefault(Font,      "font",      "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment", "CenterLeft")
	
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateTextEntry(self, data)

class TextMonitorNode(Node):
	def __init__(self, name=None, layout={}):
		super(TextMonitorNode, self).__init__("TextMonitor", name=name, layout=layout)
	
		self.setDefault(String,    "pv",           "")
		self.setDefault(Color,     "border-color", "$000000")
		self.setDefault(Number,    "border-width", 0)
		self.setDefault(Font,      "font",         "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",    "CenterLeft")
	
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateTextMonitor(self, data)

class MenuNode(Node):
	def __init__(self, name=None, layout={}):
		super(MenuNode, self).__init__("Menu", name=name, layout=layout)
	
		self.setDefault(String, "pv", "")
	
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateMenu(self, data)
	
class ChoiceButtonNode(Node):
	def __init__(self, name=None, layout={}):
		super(ChoiceButtonNode, self).__init__("ChoiceButton", name=name, layout=layout)
	
		self.setDefault(String, "pv",         "")
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(Color,  "background", "$C8C8C8")
		self.setDefault(Color,  "selected",   self["background"])
	
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateChoiceButton(self, data)
	
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
	
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateLED(self,data)

	
class ByteMonitorNode(Node):
	def __init__(self, name=None, layout={}):
		super(ByteMonitorNode, self).__init__("ByteMonitor", name=name, layout=layout)
		
		self.setDefault(String,  "pv",          "")
		self.setDefault(Bool,    "horizontal",  True)
		self.setDefault(Number,  "start-bit",   0)
		self.setDefault(Number,  "bits",        (32 - int(self["start-bit"])))
		self.setDefault(Color,   "off-color",   "$3C643C")
		self.setDefault(Color,   "on-color",    "$00FF00")

	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateByteMonitor(self, data)
	

class RectangleNode(Node):
	def __init__(self, name=None, layout={}):
		super(RectangleNode, self).__init__("Rectangle", name=name, layout=layout)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateRectangle(self, data)
	
		
class EllipseNode(Node):
	def __init__(self, name=None, layout={}):
		super(EllipseNode, self).__init__("Ellipse", name=name, layout=layout)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateEllipse(self, data)
	

class ArcNode(Node):
	def __init__(self, name=None, layout={}):
		super(ArcNode, self).__init__("Arc", name=name, layout=layout)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)
		self.setDefault(Number, "start-angle", 0)
		self.setDefault(Number, "span", 90)
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateArc(self, data)

		
class ImageNode(Node):
	def __init__(self, name=None, layout={}):
		super(ImageNode, self).__init__("Image", name=name, layout=layout)
		
		self.setDefault(String, "file", "")
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateImage(self, data)

		
class SliderNode(Node):
	def __init__(self, name=None, layout={}):
		super(SliderNode, self).__init__("Slider", name=name, layout=layout)
		
		self.setDefault(Bool,   "horizontal", True)
		self.setDefault(String, "pv",         "")
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateSlider(self, data)
		

class ScaleNode(Node):
	def __init__(self, name=None, layout={}):
		super(ScaleNode, self).__init__("Scale", name=name, layout=layout)
		
		self.setDefault(String, "pv",          "")
		self.setDefault(Color,  "background",  "$C0C0C0")
		self.setDefault(Color,  "foreground",  "$0000FF")
		self.setDefault(Bool,   "horizontal",  False)
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateScale(self, data)

		
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
		
		
	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generateShellCommand(self, data)
		

class PolygonNode(Node):
	def __init__(self, name=None, layout={}):
		self.points = layout.pop("points", [])
		
		super(PolygonNode, self).__init__("Polygon", name=name, layout=layout)
		
		self.setDefault(Color,  "background",   "$00000000")
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)

	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generatePolygon(self, data)

		
class PolylineNode(Node):
	def __init__(self, name=None, layout={}):
		self.points = layout.pop("points", [])
		
		super(PolylineNode, self).__init__("Polyline", name=name, layout=layout)
		
		self.setDefault(Color,  "border-color", "$000000")
		self.setDefault(Number, "border-width", 2)

	def apply(self, generator, data={}):
		self.updateProperties(macros=data)
		return generator.generatePolyline(self, data)
		
		
