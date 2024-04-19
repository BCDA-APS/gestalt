from gestalt.Type import *

from gestalt.convert.phoebus.CSSWidget import CSSWidget

class CSSGroup(CSSWidget):
	def __init__(self):
		super(CSSGroup, self).__init__("Group")

	def write(self, screen):
		for child in self.children:
			my_geom = self["geometry"].val()
			child_geom = child["geometry"].val()
			
			child.position(x=my_geom["x"] + child_geom["x"], y=my_geom["y"] + child_geom["y"])
			
			child.write(screen)
