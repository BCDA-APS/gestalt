from phoebusgen import screen

from gestalt.Generator import GestaltGenerator
from gestalt.Type import *

from gestalt.convert.phoebus.CSSWidget import CSSWidget
from gestalt.convert.phoebus.CSSGroup import CSSGroup

class CSSTabbedGroup(CSSWidget):
	
	def __init__(self, node=None, macros={}):
		super(CSSTabbedGroup, self).__init__("Group", node=node, macros=macros)
		
		self.widget.transparent(True)
		self.widget.no_style()
		
		self.font = self["font"]
		self.font_color = self["foreground"]
		self.tab_color = self["tab-color"]
		
		self.tab_offset = int(self["inset"])
		self.tab_padding = int(self["padding"])
		self.content_offset = int(self["offset"])
		
		self.border_width = self["border-width"]
		self.border_color = self["border-color"]
		self.select_color = self["selected"]
		self.background = self["background"]

		self.pv_name = "loc://" + self.name + "<VLong>(0)"
		
		the_font = self.font.val()
		
		self.index = 0
	
	def write(self, screen):
		self.pop("font")
		self.pop("foreground")
		self.pop("tab-color")
		self.pop("inset")
		self.pop("padding")
		self.pop("offset")
		self.pop("border-width")
		self.pop("border-color")
		self.pop("border-style")
		self.pop("selected")
		self.pop("background")
		
		super(CSSTabbedGroup, self).write(screen)
		
		
	def place(self, child, x=None, y=None, keep_original=False):
		
		self.content_offset = int(self["tabbar-height"])
		self.tab_height = self.content_offset - int(self["offset"])
		
		the_font = self.font.val()
		
		tab_width = GestaltGenerator.get_text_width(the_font["family"], int(the_font["size"]), child.name) + 10
				
		next_tab = CSSWidget("ActionButton", name=child.name + "_tab")
		next_tab["geometry"] = Rect("{x}x{y}x{wid}x{hei}".format(x=int(self.tab_offset), y=0, wid=int(tab_width), hei=int(self.tab_height)))
		next_tab["font"] = self.font
		next_tab["foreground"] = self.font_color
		next_tab["background"] = self.tab_color
		next_tab["text"] = child.name
		next_tab["pv"] = self.pv_name
		next_tab.widget.action_write_pv("$(pv_name)", self.index)
		next_tab.widget.rule(
			"selected_background", 
			"background_color", 
			{ "$(pv_name)" : True }, 
			{ "pv0==" + str(self.index) : (self.select_color["red"], self.select_color["green"], self.select_color["blue"], self.select_color["alpha"]) })
		
		intermediary = CSSGroup()
		intermediary["geometry"] = Rect("{x}x{y}x{wid}x{hei}".format(x=0, y=self.content_offset, wid=self["geometry"]["width"], hei=self["geometry"]["height"] - self.content_offset))
		intermediary["border-color"] = self.border_color
		intermediary["border-width"] = self.border_width
		#intermediary["border-style"] = self.pop("border-style", "Solid")
		intermediary["background"] = self.background
		intermediary.widget.rule("visibility", "visible", { self.pv_name : True }, {"pv0!=" + str(self.index) : False})
		
		intermediary.place(child, x=0, y=0, keep_original=keep_original)
		
		self.append(next_tab)
		self.append(intermediary)
		
		self.index += 1
		self.tab_offset = self.tab_offset + tab_width + self.tab_padding
