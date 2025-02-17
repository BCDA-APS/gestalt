from phoebusgen import screen

from gestalt.Type import *

from gestalt.Node import GroupNode

class CSSDisplay(GroupNode):
	def __init__(self, layout={}):
		super(CSSDisplay, self).__init__("")
		
	def writeCSS(self, filename):
		self.form = screen.Screen(str(String(self.pop("title", ""))))
		
		margins = Rect(self.pop("margins", "0x0x0x0"))
		
		self.form.width(  self["geometry"]["width"] )
		self.form.height( self["geometry"]["height"] )
		
		col = None
		
		if "background_color" in self:
			col = self["background_color"].val()
		elif "background" in self:
			col = self["background"].val()
		else:
			col = Color("$BBBBBB").val()
		
		self.form.background_color(col["red"], col["green"], col["blue"], col["alpha"])
		
		for child in self.children:	
			child.write(self.form)
		
		#self.write(self.form)
		self.form.write_screen(file_name=filename)
		
