from gestalt.Generator import GestaltGenerator
from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtTabbedGroup(QtWidget):
	def __init__(self, node=None, macros={}):
		super(QtTabbedGroup, self).__init__("QTabWidget", node=node, macros=macros)
		
	def write(self, tree):		
		stylesheet = ""
		
		tab_offset = self.pop("inset")
		
		stylesheet += """\
QTabWidget::tab-bar
{{
    left: {inset}px;
}}

""".format( inset=int(tab_offset) )
		
	
		the_font = self["font"].val()
	
		tab_color      = self.pop("tab-color")
		font_color     = self.pop("foreground")
		tab_padding    = self.pop("padding")
		content_offset = self.pop("offset")
		
		stylesheet += """\
QTabBar::tab
{{
    margin-right: {margin}px;
    margin-bottom: {offset}px;
	
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 5px;
    padding-right: 5px;
    
    height: {tab_height}px;
	
    background: rgba({br},{bg},{bb},{ba});
    color: rgba({tr},{tg},{tb},{ta});
}}

QTabBar::tab:hover
{{
    color: rgba({br},{bg},{bb},{ba});
    background: rgba({tr},{tg},{tb},{ta});
}}

""".format( 
	margin = int(tab_padding),
	offset = int(content_offset),
	tab_height = 9 + GestaltGenerator.get_font_height(the_font["family"], int(the_font["size"])),
	br = int(tab_color["red"]),
	bg = int(tab_color["green"]),
	bb = int(tab_color["blue"]),
	ba = int(tab_color["alpha"]),
	tr = int(font_color["red"]),
	tg = int(font_color["green"]),
	tb = int(font_color["blue"]),
	ta = int(font_color["alpha"]))
		

		border_width = self.pop("border-width")
		border_color = self.pop("border-color")
	
		stylesheet += """\
QTabWidget::pane
{{
    border-style: solid;
    border-width: {width}px;
    border-color: rgba({bor},{bog},{bob},{boa});
}}

""".format(
	width = int(border_width),
	bor = int(border_color["red"]),
	bog = int(border_color["green"]),
	bob = int(border_color["blue"]),
	boa = int(border_color["alpha"]))
		
	
		select_color = self.pop("selected")
			
		stylesheet += """\
QTabBar::tab:selected
{{
    background: rgba({selr},{selg},{selb},{sela});
}}

""".format(
	selr = int(select_color["red"]),
	selg = int(select_color["green"]),
	selb = int(select_color["blue"]),
	sela = int(select_color["alpha"]))
		
		
		background   = self.pop("background")
		
		stylesheet += """\
QWidget[Fill="True"] 
{{ 
    background: rgba({bgr},{bgg},{bgb},{bga});
}}
""".format(
	bgr = int(background["red"]),
	bgg = int(background["green"]),
	bgb = int(background["blue"]),
	bga = int(background["alpha"]))
	
		
		self["styleSheet"] = String(stylesheet)
		self["currentIndex"] = Number(0)
		
		super(QtTabbedGroup, self).write(tree)
		
	def place(self, child, x=None, y=None, keep_original=False):
		intermediary = QtWidget("QWidget", name=child.name + "_tab")
		
		intermediary["title"] = String(child.name)
		intermediary["Fill"] = String("True")
		
		intermediary.place(child, x, y, keep_original)
		self.append(intermediary)

		
		
		
		
		
		
		
		
		
		
		
		
		
