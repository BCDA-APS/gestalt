from phoebusgen import screen

from gestalt.Type import *

from gestalt.Node import GroupNode
from gestalt.convert.phoebus.CSSAnonymous   import CSSAnonymous

class CSSDisplay(CSSAnonymous):
	def __init__(self, layout={}):
		super(CSSDisplay, self).__init__()
		
		self.tocopy.append("content")
		
		self.content = CSSAnonymous()
		
	def place(self, child, x=None, y=None, keep_original=False):
		self.content.place(child, x=x, y=y, keep_original=keep_original)
		
	def writeCSS(self, filename):
		self.form = screen.Screen(str(String(self.pop("title", ""))))
		
		margins = Rect(self.pop("margins", "0x0x0x0"))
		
		self.form.width(int(self.content["geometry"]["width"] + margins["x"] + margins["width"]))
		self.form.height(int(self.content["geometry"]["height"] + margins["y"] + margins["height"]))
		
		self.content["geometry"]["x"] = margins["x"]
		self.content["geometry"]["y"] = margins["y"]
		
		col = None
		
		if "background_color" in self:
			col = self["background_color"].val()
		elif "background" in self:
			col = self["background"].val()
		else:
			col = Color("$BBBBBB").val()
		
		self.form.background_color(col["red"], col["green"], col["blue"], col["alpha"])
		
		self.content.write(self.form)
		
		for child in self.children:	
			child.write(self.form)
		
		#self.write(self.form)
		self.form.write_screen(file_name=filename)
		
