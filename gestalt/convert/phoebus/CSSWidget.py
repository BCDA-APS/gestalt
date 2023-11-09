from gestalt.Type import *

from gestalt.Node import GroupNode

from phoebusgen import widget
from phoebusgen.widget import properties as _p

name_numbering = {}


class CSSWidget(GroupNode):
	def __init__(self, classname, name=None, layout=None, macros={}):
		super(CSSWidget, self).__init__(classname, name=name, layout=layout)
		
		self.macros = macros
		
		if name:
			self.name = name
		else:
			num = name_numbering.get(classname, 0)
			num += 1
			name_numbering[classname] = num
			
			self.name = classname + str(num)
			
		if   (self.classname == "ActionButton"):
			self.widget = widget.ActionButton(self.name, "", "", 0, 0, 0, 0)
		elif (self.classname == "Arc"):
			self.widget = widget.Arc(self.name, 0, 0, 0, 0)
		elif (self.classname == "Array"):
			self.widget = widget.Array(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "BooleanButton"):
			self.widget = widget.BooleanButton(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "ByteMonitor"):
			self.widget = widget.ByteMonitor(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "CheckBox"):
			self.widget = widget.CheckBox(self.name, "", "", 0, 0, 0, 0)
		elif (self.classname == "ChoiceButton"):
			self.widget = widget.ChoiceButton(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "ComboBox"):
			self.widget = widget.ComboBox(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "DataBrowser"):
			self.widget = widget.DataBrowser(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Ellipse"):
			self.widget = widget.Ellipse(self.name, 0, 0, 0, 0)
		elif (self.classname == "EmbeddedDisplay"):
			self.widget = widget.EmbeddedDisplay(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "FileSelector"):
			self.widget = widget.FileSelector(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Group"):
			self.widget = widget.Group(self.name, 0, 0, 0, 0)
		elif (self.classname == "Image"):
			self.widget = widget.Image(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "LED"):
			self.widget = widget.LED(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "LEDMultiState"):
			self.widget = widget.LEDMultiState(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Label"):
			self.widget = widget.Label(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Meter"):
			self.widget = widget.Meter(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "NavigationTabs"):
			self.widget = widget.NavigationTabs(self.name, 0, 0, 0, 0)
		elif (self.classname == "Picture"):
			self.widget = widget.Picture(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Polygon"):
			self.widget = widget.Polygon(self.name, 0, 0, 0, 0)
		elif (self.classname == "Polyline"):
			self.widget = widget.Polylin(self.name, 0, 0, 0, 0)
		elif (self.classname == "ProgressBar"):
			self.widget = widget.ProgressBar(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "RadioButton"):
			self.widget = widget.RadioButton(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Rectangle"):
			self.widget = widget.Rectangle(self.name, 0, 0, 0, 0)
		elif (self.classname == "ScaledSlider"):
			self.widget = widget.ScaledSlider(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Scrollbar"):
			self.widget = widget.Scrollbar(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "SlideButton"):
			self.widget = widget.SlideButton(self.name, "", "", 0, 0, 0, 0)
		elif (self.classname == "Spinner"):
			self.widget = widget.Spinner(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "StripChart"):
			self.widget = widget.StripChart(self.name, 0, 0, 0, 0)
		elif (self.classname == "Symbol"):
			self.widget = widget.Symbol(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Table"):
			self.widget = widget.Table(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Tabs"):
			self.widget = widget.Tabs(self.name, 0, 0, 0, 0)
		elif (self.classname == "Tank"):
			self.widget = widget.Tank(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "TextEntry"):
			self.widget = widget.TextEntry(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "TextSymbol"):
			self.widget = widget.TextSymbol(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "TextUpdate"):
			self.widget = widget.TextUpdate(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Thermometer"):
			self.widget = widget.Thermometer(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "ThreeDViewer"):
			self.widget = widget.ThreeDViewer(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "WebBrowser"):
			self.widget = widget.WebBrowser(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "XYPlot"):
			self.widget = widget.XYPlot(self.name, 0, 0, 0, 0)	
		
			
	def write(self, screen):
		for key, item in self.attrs.items():
			item.apply(self.macros)
			
		if self.widget:
			self.widget.x(self["geometry"]["x"])
			self.widget.y(self["geometry"]["y"])
			self.widget.width(self["geometry"]["width"])
			self.widget.height(self["geometry"]["height"])
			
			if "visible" in self.attrs:
				self.widget.visible(self["visible"])
				
			if "tool_tip" in self.attrs:
				self.widget.tool_tip(self["tool_tip"])
				
			if isinstance(self.widget, _p._PVName) and "pv_name" in self.attrs:
				self.widget.pv_name(self["pv_name"].val)
				
			if isinstance(self.widget, _p._Text) and "text" in self.attrs:
				self.widget.text(self["text"].val)
				
				
		for child in self.children:
			child.write(self.widget)
			
		screen.add_widget(self.widget)
