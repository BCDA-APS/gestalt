from lxml.etree import ElementTree, TreeBuilder

from gestalt import Stylesheet
from gestalt import Datasheet
from gestalt.Type import *

import copy
import yaml

name_numbering = {}


class Node(object):
	def __init__(self, classname, name=None, initial=None, layout=None, expands=False):
		self.classname = classname
		self.name = None
		self.expands = expands
		
		self.attrs = {"geometry" : Rect(x=0, y=0, width=0, height=0)}
		self.children = []
		
		if name is not None:
			self.name = name
		
		if layout is not None:
			self.setProperties(layout)
			
		if initial is not None:
			if isinstance(initial, dict):
				for childname, child in initial.items():
					child.name = childname
					self.append(child)
				
			elif isinstance(initial, list) or isinstance(initial, tuple):
				for child in initial:
					self.append(child)
					
					
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

		
	def append(self, child, keep_original=False):
		if not keep_original:
			cpy = copy.deepcopy(child)
		
			self.children.append(cpy)
			
		else:
			self.children.append(child)
			
		if self.expands:
			right_edge  = child["geometry"]["x"] + child["geometry"]["width"]
			bottom_edge = child["geometry"]["y"] + child["geometry"]["height"]
			
			if right_edge > self["geometry"]["width"]:
				self["geometry"]["width"] = right_edge
				
			if bottom_edge > self["geometry"]["height"]:
				self["geometry"]["height"] = bottom_edge
				
			
		return self
		
		
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
		output = QtWidget(self.classname, name=self.name, layout=self.attrs, macros=data)
		
		for childnode in self.children:
			output.append(childnode.generateQt(data))
		
		return output

		
class RepeatNode(Node):
	def __init__(self, initial=None, name=None, layout=None, repeat=None):
		super(RepeatNode, self).__init__("caFrame", initial=initial, name=name, layout=layout, expands=False)
		
		self.repeat_over = repeat
	
		
	def generateQt (self, data={}):		
		macrolist = data.get(self.repeat_over, None)
		
		output = QtWidget("caFrame", name=self.name, layout=self.attrs, macros=data, expands=True)
		
		for macroset in macrolist:
			line = QtWidget("caFrame", expands=True)
			
			for childnode in self.children:
				line.append(childnode.generateQt(macroset))
			
			line.position(x=0, y=output["geometry"]["height"])
				
			output.append(line)
			
		return output

		
		
class QtWidget(Node):
	def __init__(self, classname, initial=None, name=None, layout=None, macros={}, expands=False):
		super(QtWidget, self).__init__(classname, initial=initial, name=name, layout=layout, expands=expands)
	
		self.macros = macros
		
		if name:
			self.name = name
		else:
			num = name_numbering.get(classname, 0)
			num += 1
			name_numbering[classname] = num
			
			self.name = classname + str(num)
	
		
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
		tree = TreeBuilder()
		
		tree.start("ui", {"version" : "4.0"})
		tree.start("class", {})
		tree.data("Form")
		tree.end("class")
		
		self.form.write(tree)
		
		tree.end("ui")
		
		writer = ElementTree(element=tree.close())
		writer.write(filename, pretty_print=True)

		
		
		
		
def generateQtFile(stylesheet="", datafile="", outputfile=""):
	a_display = QtDisplay()
	styles = Stylesheet.parse(stylesheet)
	data = Datasheet.parse(datafile)
	
	for key, item in styles.items():
		if isinstance(item, Node):
			if item.classname == "Form":
				a_display.setProperties(item.attrs)
			else:
				a_display.append(item.generateQt(data))
				
	a_display.writeQt(outputfile)
