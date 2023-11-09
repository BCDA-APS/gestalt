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
			tree.start("property", {"name" : key})
			item.write(tree, self.macros)
			tree.end("property")
						
		for child in self.children:
			child.write(tree)
			
		tree.end("widget")
