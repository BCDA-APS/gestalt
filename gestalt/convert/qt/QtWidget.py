from gestalt.Type import *

from gestalt.Node import GroupNode

name_numbering = {}

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
			
			
	def write(self, tree):
		tree.start("widget", {"class" : self.classname, "name" : self.name})
			
		for key, item in self.attrs.items():
			item.apply(self.macros)
			
			tree.start("property", {"name" : key})
				
			if isinstance(item, Color):
				tree.start("color", {"alpha" : str(item.val["alpha"])})
		
				for component, value in item.val.items():
					if component != "alpha":
						tree.start(component, {})
						tree.data(str(value))
						tree.end(component)
					
				tree.end("color")
			
			elif isinstance(item, Bool):
				tree.start("bool", {})
				
				if item.val:
					tree.data("true")
				else:
					tree.data("false")
					
				tree.end("bool")
				
			elif isinstance(item, Font):
				tree.start("font")
				
				tree.start("family")
				tree.data(str(item["family"]))
				tree.end("family")
				
				if item["size"]:
					tree.start("pointsize")
					tree.data(str(item["size"]))
					tree.end("pointsize")
					
				if item["style"]:
					if "bold" in item["style"]:
						tree.start("bold")
						tree.data("true")
						tree.end("bold")
						
					if "italic" in item["style"]:
						tree.start("italic")
						tree.data("true")
						tree.end("italic")
					
				tree.end("font")
			
			else:
				tree.start(item.typ, {})
		
				if (type(item.val) is dict):
					for component, value in item.val.items():
						tree.start(component, {})
						tree.data(str(value))
						tree.end(component)
				else:
					tree.data(str(item.val))
					
				tree.end(item.typ)
				
			tree.end("property")
						
		for child in self.children:
			child.write(tree)
			
		tree.end("widget")
