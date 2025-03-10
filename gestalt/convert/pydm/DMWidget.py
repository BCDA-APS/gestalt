from gestalt.Type import *
from gestalt.convert.pydm.DMTypes import *

from gestalt.Generator import GestaltGenerator
from gestalt.Node import GroupNode

import json

stdset = [ "channel", "filename", "pressValue" ]
notr   = [ "styleSheet" ]

name_numbering = {}
local_pvs = []

def reset_numbering():
	name_numbering = {}
	
def add_local_pv(name):
	global local_pvs
	
	local_pvs.append(name)
	
def get_pv(pvname):
	global local_pvs
	
	output = pvname
	
	if pvname in local_pvs:
		output = "calc://pv_" + pvname
		
	return output


class DMWidget(GroupNode):
	def __init__(self, classname, node=None, name=None, layout={}, macros={}, loc=None):		
		super(DMWidget, self).__init__(classname, name=name, node=node, layout=layout, loc=loc)
		DMWidget.updateProperties(self, macros)
		
		self.styleWriters = []
		self.toRemove = [ "border-width" ]

		self.tocopy.append("styleWriters")
		self.tocopy.append("toRemove")
		
		if "alignment" in self and not isinstance(self["alignment"], Set):
			data = str(Alignment(self.pop("alignment")))
			
			# Split into two strings based on capitalization
			data = "".join([(" "+i if i.isupper() else i) for i in data]).strip().split()
			
			valign = "Qt::Align" + data[0]
			halign = "Qt::Align" + data[1]
				
			if halign == "Qt::AlignCenter":
				halign = "Qt::AlignHCenter"
				
			if valign == "Qt::AlignCenter":
				valign = "Qt::AlignVCenter"
				
			self["alignment"] = Set(halign + "|" + valign)				
	
		if not self.name:
			num = name_numbering.get(classname, 0)
			num += 1
			name_numbering[classname] = num
			
			self.name = classname + str(num)
			
		else:
			num = name_numbering.get(self.name, 0)
			num += 1
			name_numbering[self.name] = num
			
			if (num > 1):
				self.name = self.name + str(num)

	def addStyleWriter(self, writer):
		self.styleWriters.append(writer)
				
	def write(self, tree):
		stylesheet = ""
		
		for writer in self.styleWriters:
			stylesheet += writer(self)
			
		self["styleSheet"] = String(stylesheet)
		
		if "font" in self:
			my_font = self["font"]
			font_size = GestaltGenerator.get_size_for_height(my_font["family"], int(self["geometry"]["height"]))
			my_font["size"] = font_size
			self["font"] = my_font
	
		for item in self.toRemove:
			self.pop(item)
		
		tree.start("widget", {"class" : self.classname, "name" : self.name})
		
		for key, item in self.properties["attrs"].items():
			if key == "visibility":
				tree.start("property", {"name" : "rules", "stdset" : "0"})
				tree.start("string", {})
				
				vis_pv = self["visibility"]
				vis_zero = isinstance(vis_pv, Not)
				
				output = {}
				output["name"] = "visibility"
				output["property"] = "Visible"
				output["initial_value"] = "true"
				output["notes"] = ""
				
				if vis_zero:
					output["expression"] = "ch[0]==0"
				else:
					output["expression"] = "ch[0]!=0"
					
				channel = {}
				channel["trigger"] = True
				channel["use_enum"] = False
				channel["channel"] = get_pv(str(vis_pv))
				
				output["channel"] = [channel]
					
				tree.data(json.dumps([output]))
				
				tree.end("string")
			elif isinstance(item, Brush):
				tree.start("property", {"name" : key, "stdset" : "0"})
				tree.start("brush", {"brushstyle" : "SolidPattern"})
				tree.start("color", {"alpha" : str(item.val()["alpha"])})
		
				for component, value in item.val().items():
					if component != "alpha":
						tree.start(component, {})
						tree.data(str(value))
						tree.end(component)
					
				tree.end("color")
				tree.end("brush")
				
			elif isinstance(item, Color):
				tree.start("property", {"name" : key, "stdset" : "0"})
				tree.start("color", {"alpha" : str(item.val()["alpha"])})
		
				for component, value in item.val().items():
					if component != "alpha":
						tree.start(component, {})
						tree.data(str(value))
						tree.end(component)
					
				tree.end("color")
			
			elif isinstance(item, Bool):
				tree.start("property", {"name" : key, "stdset" : "0"})
				tree.start("bool", {})
				
				if bool(item):
					tree.data("true")
				else:
					tree.data("false")
					
				tree.end("bool")
				
			elif isinstance(item, Font):
				tree.start("property", {"name" : key})
				tree.start("font", {})
				
				tree.start("family", {})
				tree.data(str(item["family"]))
				tree.end("family")
				
				if item["size"]:
					tree.start("pointsize", {})
					tree.data(str(item["size"]))
					tree.end("pointsize")
					
				if item["style"]:					
					if "bold" in item["style"].lower():
						tree.start("bold", {})
						tree.data("true")
						tree.end("bold")
						
					if "italic" in item["style"].lower():
						tree.start("italic", {})
						tree.data("true")
						tree.end("italic")
					
				tree.end("font")
			elif isinstance(item, List):
				tree.start("property", {"name" : key, "stdset" : "0"})
				tree.start("stringlist", {})
				
				for a_string in item:
					tree.start("string", {})
					tree.data(str(a_string))
					tree.end("string")
					
				tree.end("stringlist")
				
			else:
				if key == "title":
					tree.start("attribute", {"name" : key})
				else:
					if isinstance(item, Enum) or isinstance(item, Number) or key in stdset:
						tree.start("property", {"name" : key, "stdset" : "0"})
					else:
						tree.start("property", {"name" : key})
					
				if key in notr:
					tree.start(item.typ, {"notr" : "true"})
				else:
					tree.start(item.typ, {})
		
				if (type(item.val()) is dict):
					for component, value in item.val().items():
						tree.start(component, {})
						tree.data(str(value))
						tree.end(component)
				else:
					tree.data(str(item.val()))
					
				tree.end(item.typ)
				
			if key == "title":
				tree.end("attribute")
			else:
				tree.end("property")
						
		for child in self.children:
			child.write(tree)
			
		tree.end("widget")
