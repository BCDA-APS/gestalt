from gestalt.Type import *

from gestalt.Node import GroupNode

from gestalt.convert.phoebus.CSSWidget import CSSWidget

from phoebusgen import widget
from phoebusgen.widget import properties as _p

class CSSGroup(CSSWidget):
	def __init__(self, name=None, layout={}, macros={}):
		super(CSSGroup, self).__init__("Group", name=name, layout=layout)
		
		self.widget.transparent(True)
		self.widget.no_style()
	
	def write(self, screen):
		frame = CSSWidget("Rectangle")
		frame.attrs["geometry"]["width"] = self["geometry"]["width"]
		frame.attrs["geometry"]["height"] = self["geometry"]["height"]
		frame.attrs["background"] = Color("$00000000")
		frame.attrs["line"] = Color("$000000FF")
		frame.attrs["line_width"] = Number(0)
		
		frame.attrs["line"] = Color(self.attrs.pop("border-color", "$00000000"))			
		frame.attrs["line_width"] = Number(self.attrs.pop("border-width", 2))
		frame.attrs["background"] = Color(self.attrs.pop("background", "$00000000"))
		
		frame.write(self.widget)
			
		super(CSSGroup, self).write(screen)
		
