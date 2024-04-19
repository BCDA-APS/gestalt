from gestalt.Type import *

from gestalt.convert.phoebus.CSSWidget import CSSWidget

class CSSGroup(CSSWidget):
	def __init__(self, node=None, macros={}):
		super(CSSGroup, self).__init__("Group", node=node, macros=macros)
		
		self.widget.transparent(True)
		self.widget.no_style()
	
	def write(self, screen):
		frame = CSSWidget("Rectangle")
		frame["geometry"]["width"] = self["geometry"]["width"]
		frame["geometry"]["height"] = self["geometry"]["height"]
		frame["background"] = Color("$00000000")
		frame["line"] = Color("$000000FF")
		frame["line_width"] = Number(0)
		
		frame["line"] = Color(self.pop("border-color", "$000000"))
		frame["line_width"] = Number(self.pop("border-width", 0))
		frame["background"] = Color(self.pop("background", "$00000000"))
		
		if ( (int(frame["line_width"]) != 0 and frame["background"].val()["alpha"] != 0) or frame["background"].val()["alpha"] != 0):
			self.children.insert(0, frame)
			
		super(CSSGroup, self).write(screen)
		
