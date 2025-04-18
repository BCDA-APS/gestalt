from gestalt.Type import *

from gestalt.nodes.GroupNode import GroupNode

name_numbering = {}

def reset_numbering():
	name_numbering = {}

class QtWidget(GroupNode):
	def __init__(self, classname, node=None, name=None, layout={}, macros={}, loc=None):		
		super(QtWidget, self).__init__(classname, name=name, node=node, layout=layout, loc=loc)
		QtWidget.updateProperties(self, macros)
		
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
	
		
		if "visibility" in self and not isinstance(self["visibility"], Enum):	
			vis_pv = self.pop("visibility", None)
			vis_zero = isinstance(vis_pv, Not)
				
			self["channel"] = String(vis_pv)
			
			if vis_zero:
				self["visibility"] = Enum(classname + "::IfZero")
			else:
				self["visibility"] = Enum(classname + "::IfNotZero")
			
	
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
			
	def write(self, tree):
		# Border-width is default in GroupNode
		self.pop("border-width")
		
		tree.start("widget", {"class" : self.classname, "name" : self.name})
		
		for key, item in self.properties["attrs"].items():
			if key == "title":
				tree.start("attribute", {"name" : key})
			else:
				tree.start("property", {"name" : key})
				
			if isinstance(item, Color):
				tree.start("color", {"alpha" : str(item.val()["alpha"])})
		
				for component, value in item.val().items():
					if component != "alpha":
						tree.start(component, {})
						tree.data(str(value))
						tree.end(component)
					
				tree.end("color")
			
			elif isinstance(item, Bool):
				tree.start("bool", {})
				
				if bool(item):
					tree.data("true")
				else:
					tree.data("false")
					
				tree.end("bool")
				
			elif isinstance(item, Font):
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
						
		for child in self.write_order():
			child.write(tree)
			
		tree.end("widget")
