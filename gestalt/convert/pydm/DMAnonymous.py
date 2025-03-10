from gestalt.Type import *

from gestalt.convert.pydm.DMWidget import DMWidget

class DMAnonymous(DMWidget):
	def __init__(self):
		super(DMAnonymous, self).__init__("anonymous")
		
		
	def write(self, tree):
		for child in self.children:
			my_geom = self["geometry"].val()
			child_geom = child["geometry"].val()
			
			child.position(x=my_geom["x"] + child_geom["x"], y=my_geom["y"] + child_geom["y"])
			
			child.write(tree)
	
