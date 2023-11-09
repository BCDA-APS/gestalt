from lxml.etree import ElementTree, TreeBuilder

from gestalt import Stylesheet
from gestalt import Datasheet
from gestalt.Type import *

import math
import string

import copy
import yaml

name_numbering = {}


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
			if instanceof(args[0], list) or instanceof(args[0], tuple):
				out_x = args[0][0]
				out_y = args[0][1]
			elif instanceof(args[0], dict):
				out_x = args[0]["x"]
				out_y = args[0]["y"]				
		
		self.setProperty("geometry", Rect(x = out_x, y = out_y))
				
		return self

		
	def generateQt (self, data={}):
		return QtWidget(self.classname, name=self.name, layout=self.attrs, macros=data)
		
		
		
class GroupNode(Node):
	def __init__(self, classname, initial=None, name=None, layout=None):
		super(GroupNode, self).__init__(classname, name=name, layout=layout)
	
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
			
		return self
		
	
	def generateQt (self, data={}):
		output = QtWidget(self.classname, name=self.name, layout=self.attrs, macros=data)
				
		child_macros = copy.deepcopy(data)
		
		for child in self.children:
			child_macros.update({
				"__parentx__" : output["geometry"]["x"],
				"__parenty__" : output["geometry"]["y"],
				"__parentwidth__" : output["geometry"]["width"],
				"__parentheight__" : output["geometry"]["height"]})
				
			output.append(child.generateQt(child_macros))
			
		return output

		
class GridNode(GroupNode):
	def __init__(self, initial=None, name=None, layout=None, padding=0, repeat=None, ratio=1.0):
		super(GridNode, self).__init__("caFrame", initial=initial, name=name, layout=layout)
		
		self.ratio = ratio
		self.repeat_over = repeat
		self.padding = padding
		
		
	def generateQt (self, data={}):
		macrolist = data.get(self.repeat_over, {})
		
		output = QtWidget("caFrame", name=self.name, layout=self.attrs, macros=data)
		
		num_items = len(macrolist)
		
		rows = round(math.sqrt(num_items * self.ratio))
		cols = round(math.sqrt(num_items / self.ratio))
		
		index = 0
		index_x = 0
		index_y = 0
		
		for macroset in macrolist:
			child_macros = copy.deepcopy(data)
			child_macros.update(macroset)
			child_macros.update({"__index__" : index})
			
			element = QtWidget("caFrame")
			
			for childnode in self.children:
				child_macros.update({
					"__parentx__" : self["geometry"]["x"],
					"__parenty__" : self["geometry"]["y"],
					"__parentwidth__" : self["geometry"]["width"],
					"__parentheight__" : self["geometry"]["height"]})
					
				element.append(childnode.generateQt(child_macros))
			
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
	
		
	def generateQt (self, data={}):		
		macrolist = data.get(self.repeat_over, None)
		
		output = QtWidget("caFrame", name=self.name, layout=self.attrs, macros=data)
		
		first = True
		
		for macroset in macrolist:
			child_macros = copy.deepcopy(data)
			
			child_macros.update(macroset)
			
			line = QtWidget("caFrame")
			
			for childnode in self.children:
				child_macros.update({
					"__parentx__" : self["geometry"]["x"],
					"__parenty__" : self["geometry"]["y"],
					"__parentwidth__" : self["geometry"]["width"],
					"__parentheight__" : self["geometry"]["height"]})
					
				line.append(childnode.generateQt(child_macros))
			
			if self.flow == "vertical":
				if first:
					line.position(x=0, y=output["geometry"]["height"])
					first = False
				else:
					line.position(x=0, y=output["geometry"]["height"] + self.padding)
				
			elif self.flow == "horizontal":
				if first:
					line.position(x=output["geometry"]["width"], y=0)
					first = False
				else:
					line.position(x=output["geometry"]["width"] + self.padding, y=0)
				
			output.append(line)
			
		return output

		
class StretchNode(Node):
	def __init__(self, name=None, layout=None, flow="vertical", subnode=None):
		super(StretchNode, self).__init__("Stretch", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def generateQt (self, data={}):		
		if self.flow == "vertical":
			self.subnode["geometry"]["height"] = data["__parentheight__"]
		elif self.flow == "horizontal":
			self.subnode["geometry"]["width"] = data["__parentwidth__"]
		
		return self.subnode.generateQt(data)

class CenterNode(Node):
	def __init__(self, name=None, layout=None, flow="vertical", subnode=None):
		super(CenterNode, self).__init__("Center", name=name, layout=layout)
		
		self.subnode = subnode
		self.flow = flow
		
	def generateQt (self, data={}):
		qtnode = self.subnode.generateQt(data)
			
		if self.flow == "vertical":
			qtnode.position(qtnode["geometry"]["x"], int(data["__parentheight__"] / 2) - int(qtnode["geometry"]["height"] / 2))
		elif self.flow == "horizontal":
			qtnode.position(int(data["__parentwidth__"] / 2) - int(qtnode["geometry"]["width"] / 2), qtnode["geometry"]["y"])
					
		return qtnode

		
		
class QtWidget(GroupNode):
	def __init__(self, classname, initial=None, name=None, layout=None, macros={}):
		super(QtWidget, self).__init__(classname, initial=initial, name=name, layout=layout)
	
		self.macros = macros
		
		if name:
			self.name = name
		else:
			num = name_numbering.get(classname, 0)
			num += 1
			name_numbering[classname] = num
			
			self.name = classname + str(num)
	
	def append(self, child, keep_original=True):
		super(QtWidget, self).append(child, keep_original=keep_original)
			
		right_edge  = child["geometry"]["x"] + child["geometry"]["width"]
		bottom_edge = child["geometry"]["y"] + child["geometry"]["height"]
		
		if right_edge > self["geometry"]["width"]:
			self["geometry"]["width"] = right_edge
			
		if bottom_edge > self["geometry"]["height"]:
			self["geometry"]["height"] = bottom_edge
			
			
	def write(self, tree):
		tree.start("widget", {"class" : self.classname, "name" : self.name})
		
		for key, item in self.attrs.items():
			tree.start("property", {"name" : key})
			item.write(tree, self.macros)
			tree.end("property")
						
		for child in self.children:
			child.write(tree)
			
		tree.end("widget")

		

class QtDisplay(QtWidget):
	def __init__(self, layout=None):
		super(QtDisplay, self).__init__("QWidget", name="centralwidget")
	
		self.form = QtWidget("QWidget", name="Form", layout=layout)
	
		self.form.append(self, keep_original=True)
	
		
	def setProperties(self, layout):
		self.form.setProperties(layout)
		
	def setProperty(self, key, prop):
		self.form.setProperty(key, prop)
		
		
	def writeQt(self, filename):
		margins = Rect(x=0, y=0, width=0, height=0)
		margins = margins.merge(self.form.attrs.pop("margins", Rect(x=0, y=0, width=0, height=0)))
		
		self.form["geometry"]["width"]  = self["geometry"]["width"] + margins["x"] + margins["width"]
		self.form["geometry"]["height"] = self["geometry"]["height"] + margins["y"] + margins["height"]
		
		self["geometry"]["x"] = margins["x"]
		self["geometry"]["y"] = margins["y"]
		
		tree = TreeBuilder()
		
		tree.start("ui", {"version" : "4.0"})
		tree.start("class", {})
		tree.data("Form")
		tree.end("class")
		
		self.form.write(tree)
		
		tree.end("ui")
		
		writer = ElementTree(element=tree.close())
		writer.write(filename, pretty_print=True)

		
		
		
		
def generateQtFile(stylesheet="", datafile="", datastr="", outputfile="", searchpath=""):	
	a_display = QtDisplay()
	
	includes_dirs = str.split(".:" + searchpath, ":")
	
	styles = Stylesheet.parse(stylesheet, includes_dirs)
	data = None
	
	if datafile != "":
		data = Datasheet.parseFile(datafile)
	else:
		data = Datasheet.parseString(datastr)
		
	for key, item in styles.items():
		if isinstance(item, Node):
			if item.classname == "Form":
				a_display.setProperties(item.attrs)
			else:
				data.update({
					"__parentx__" : a_display["geometry"]["x"],
					"__parenty__" : a_display["geometry"]["y"],
					"__parentwidth__" : a_display["geometry"]["width"],
					"__parentheight__" : a_display["geometry"]["height"]})
			
				a_display.append(item.generateQt(data))
				
	a_display.writeQt(outputfile)
