from lxml.etree import ElementTree, TreeBuilder

from gestalt.Type import *

from gestalt.convert.pydm.DMWidget import DMWidget

widget_info = {
	"PyDMLabel"                : { "extends" : "QLabel",            "header" : "pydm.widgets.label"     },
	"PyDMLineEdit"             : { "extends" : "QLineEdit",         "header" : "pydm.widgets.line_edit" },
	"PyDMDrawingArc"           : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingChord"         : { "extends" : "PyDMDrawingArc",    "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingCircle"        : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingEllipse"       : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingImage"         : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingLine"          : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingPie"           : { "extends" : "PyDMDrawingArc",    "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingRectangle"     : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingTriangle"      : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingPolygon"       : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMDrawingPolyline"      : { "extends" : "QWidget",           "header" : "pydm.widgets.drawing"   },
	"PyDMByteIndicator"        : { "extends" : "QWidget",           "header" : "pydm.widgets.byte"      },
	"PyDMMultiStateIndicator"  : { "extends" : "QWidget",           "header" : "pydm.widgets.byte"      },
	"PyDMSpinbox"              : { "extends" : "QDoubleSpinBox",    "header" : "pydm.widgets.spinbox"   },
	"PyDMShellCommand"         : { "extends" : "QPushButton",       "header" : "pydm.widgets.shell_command" },
	"PyDMScaleIndicator"       : { "extends" : "QFrame",            "header" : "pydm.widgets.scale"     },
	"PyDMAnalogIndicator"      : { "extends" : "PyDMScaleIndicator","header" : "pydm.widgets.analog_indicator" },
	"PyDMRelatedDisplayButton" : { "extends" : "QPushButton", "header" : "pydm.widgets.related_display_button" },
	"PyDMPushButton"           : { "extends" : "QPushButton", "header" : "pydm.widgets.pushbutton"      },
}

def write_form(node):
	bg_col = Color(node.pop("background", "$BBBBBB"))
	stylesheet_str = "QFrame#background {background-color: rgba(" + str(bg_col["red"]) + "," + str(bg_col["green"]) + "," + str(bg_col["blue"]) + "," + str(bg_col["alpha"]) + ");}"
	stylesheet_str += "\nQPushButton::menu-indicator {image: url(none.png); width: 0}"
	
	node.toRemove.append("background")
	return stylesheet_str


class DMDisplay(DMWidget):
	def __init__(self, layout={}):
		super(DMDisplay, self).__init__("QFrame", name="content")
		
		self.widg = DMWidget("QFrame", name="background")
		self.form = DMWidget("QWidget", name="Form", layout=layout)
		
		self.widg.append(self, keep_original=True)
		self.form.append(self.widg, keep_original=True)
		
		self.tocopy.append("form")
		self.tocopy.append("widg")

	def updateProperties(self, macros={}):
		self.form.updateProperties(macros)
		
	def setProperty(self, key, prop):
		self.form.setProperty(key, prop)
		
		
	def writeDM(self, filename):
		self.widg["background"] = self.form.pop("background")
		self.widg.addStyleWriter(write_form)
		
		self.form.link("windowTitle", "title")
		
		margins = Rect(self.form.pop("margins", "0x0x0x0"))
		
		check_width = self["geometry"]["width"] + margins["x"] + margins["width"]
		check_height = self["geometry"]["height"] + margins["y"] + margins["height"]
		
		if check_width > self.form["geometry"]["width"]:
			self.form["geometry"]["width"] = check_width
		
		if check_height > self.form["geometry"]["height"]:
			self.form["geometry"]["height"] = check_height
		
		self.widg["geometry"] = self.form["geometry"]
			
		self["geometry"]["x"] = margins["x"]
		self["geometry"]["y"] = margins["y"]
		
		tree = TreeBuilder()
		
		tree.start("ui", {"version" : "4.0"})
		tree.start("class", {})
		tree.data("Form")
		tree.end("class")
		
		self.form.write(tree)
		
		tree.start("customwidgets", {})
		
		for widgetclass in widget_info:
			tree.start("customwidget", {})
			
			tree.start("class", {})
			tree.data(widgetclass)
			tree.end("class")
			
			tree.start("extends", {})
			tree.data(widget_info[widgetclass]["extends"])
			tree.end("extends")
			
			tree.start("header", {})
			tree.data(widget_info[widgetclass]["header"])
			tree.end("header")
			
			tree.end("customwidget")
		
		tree.end("customwidgets")
		
		tree.end("ui")
		
		writer = ElementTree(element=tree.close())
		writer.write(filename, pretty_print=True)
