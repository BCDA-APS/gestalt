from lxml.etree import ElementTree, TreeBuilder

from phoebusgen import screen

from gestalt.Type import *

from gestalt.convert.phoebus.CSSGroup import CSSGroup

class CSSDisplay(CSSGroup):
	def __init__(self, layout=None):
		super(CSSDisplay, self).__init__()
	
		self.form = screen.Screen("Form")
		
	def writeCSS(self, filename):
		margins = Rect(x=0, y=0, width=0, height=0)
		margins = margins.merge(self.attrs.pop("margins", Rect(x=0, y=0, width=0, height=0)))
		
		self.form.width(  self["geometry"]["width"] + margins["x"] + margins["width"] )
		self.form.height( self["geometry"]["height"] + margins["y"] + margins["height"] )
		
		self["geometry"]["x"] = margins["x"]
		self["geometry"]["y"] = margins["y"]
		
		self.write(self.form)
		self.form.write_screen(file_name=filename)
		
