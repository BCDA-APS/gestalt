from gestalt.Type import *

from gestalt.Node import GroupNode

from phoebusgen import widget


class CSSGroup(GroupNode):
	def __init__(self, layout=None, macros={}):
		super(CSSGroup, self).__init__("", layout=layout)
		
		self.macros = macros
		
	def write(self, screen):
		for key, item in self.attrs.items():
			item.apply(self.macros)
					
		for child in self.children:
			child["geometry"]["x"] += self["geometry"]["x"]
			child["geometry"]["y"] += self["geometry"]["y"]
			
			
			child.write(screen)
			
		#screen.add_widget(self.widget)
