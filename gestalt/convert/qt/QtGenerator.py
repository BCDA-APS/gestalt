from gestalt.Node import *
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from gestalt.convert.qt.QtWidget import QtWidget
from gestalt.convert.qt.QtGroup  import QtGroup
from gestalt.convert.qt.QtDisplay import QtDisplay


class QtGenerator(GestaltGenerator):
	def generateWidget(self, original, macros={}):
		return QtWidget(original.classname, name=original.name, layout=original.attrs, macros=macros)
		
	def generateGroup(self, original, macros={}):
		return QtGroup(name=original.name, layout=original.attrs, macros=macros)
	
	def generateAnonymousGroup(self, macros={}):
		return QtGroup()
		
	def generateRelatedDisplay(self, node, macros={}):
		output = QtWidget("caRelatedDisplay", name=node.name, layout=node.attrs, macros=macros)
		
		output["label"] = String("-" + str(output.pop("text")))
		
		labels = ""
		files = ""
		args = ""
		replace = ""
		
		for item in node.links:
			labels += str(item.get("label", "")) + ";"
			files  += str(item.get("file", "")) + ";"
			args   += str(item.get("macros", "")) + ";"
			
			if "replace" in item and item.replace:
				replace += "true;"
			else:
				replace += "false;"

		output["labels"] = String(labels.rstrip(";"))
		output["files"]  = String(files.rstrip(";"))
		output["args"]   = String(args.rstrip(";"))
		output["removeParent"] = String(replace.rstrip(";"))
		output["stackingMode"] = Enum("Menu")
		
		return output
		
		
	def generateShellCommand(self, node, macros={}):
		output = QtWidget("caShellCommand", name=node.name, layout=node.attrs, macros=macros)
		
		output["label"] = String("-" + str(output.pop("text")))
		
		labels = ""
		commands = ""
		args = ""
		
		for item in node.commands:
			labels += str(item.get("label", "")) + ";"
			commands  += str(item.get("command", "")) + ";"
			args   += ";"
			
			
		output["labels"] = String(labels.rstrip(";"))
		output["files"]  = String(commands.rstrip(";"))
		output["args"]   = String(args.rstrip(";"))
		
		return output
		
		
	def generateMessageButton(self, node, macros={}):
		output = QtWidget("caMessageButton", name=node.name, layout=node.attrs, macros=macros)

		output.link("label", "text")
		output.link("channel", "pv")
		output.link("pressMessage", "value")
			
		output["colorMode"] = Enum("caMessageButton::Static")
			
		return output
		
		
	def generateText(self, node, macros={}):
		output = QtWidget("caLabel", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("borderColor", "border-color")
		output.link("borderWidth", "border-width")
		
		output["fontScaleMode"] = Enum("ESimpleLabel::None")
		
		return output
		
		
	def generateTextEntry(self, node, macros={}):
		output = QtWidget("caTextEntry", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
			
		output["colorMode"]     = Enum("caLineEdit::Static")
		output["fontScaleMode"] = Enum("caLineEdit::None")
		
		return output
		
		
	def generateTextMonitor(self, node, macros={}):
		output = QtWidget("caLineEdit", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		output.link("frameColor", "border-color")
		output.link("frameWidth", "border-width")
			
		output["colorMode"]     = Enum("caLineEdit::Static")
		output["fontScaleMode"] = Enum("caLineEdit::None")
		
		return output
		
		
	def generateMenu(self, node, macros={}):
		output = QtWidget("caMenu", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
			
		output["colorMode"] = Enum("caMenu::Static")
		
		return output
		
		
	def generateChoiceButton(self, node, macros={}):
		output = QtWidget("caChoice", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		output.link("bordercolor", "selected")
		
		if output.pop("horizontal"):
			output["stackingMode"] = Enum("Row")
			
		output["colorMode"] = Enum("caChoice::Static")
		
		return output
		
		
	def generateLED(self, node, macros={}):
		output = QtWidget("caLed", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		output.link("rectangular", "square")
		output.link("falseColor", "false-color")
		output.link("falseValue", "false-value")
		output.link("trueColor", "true-color")
		output.link("trueValue", "true-value")
		output.link("undefinedColor", "undefined-color")
		output.link("borderColor", "border-color")
	
		output["gradientEnabled"] = Bool(False)
		output["scaleContents"]   = Bool(True)
		
		return output
		
		
	def generateByteMonitor(self, node, macros={}):
		output = QtWidget("caByteController", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		output.link("startBit", "start-bit")
		output.link("background", "off-color")
		output.link("foreground", "on-color")
		
		if output.pop("horizontal"):
			output["direction"] = Enum("Right")
		else:
			output["direction"] = Enum("Down")
			
		num_bits = output.pop("bits")
		
		output["endBit"] = Number(int(output["startBit"]) + int(num_bits) - 1)
		
		return output
		
		
	def generateRectangle(self, node, macros={}):
		output = QtWidget("caGraphics", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		
		output["form"] = Enum("caGraphics::Rectangle")
		output["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		
	
	def generateEllipse(self, node, macros={}):
		output = QtWidget("caGraphics", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		
		output["form"] = Enum("caGraphics::Circle")
		output["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		
		
	def generateArc(self, node, macros={}):
		output = QtWidget("caGraphics", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		output.link("startAngle", "start-angle")
		output.link("spanAngle",  "span")
		
		output["form"] = Enum("caGraphics::Arc")
		output["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		
	
	def generatePolygon(self, node, macros={}):
		output = QtWidget("caPolyLine", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		
		output["polystyle"] = Enum("caPolyLine::Polygon")
		output["fillstyle"] = Enum("caPolyLine::Filled")
		
		xy_pairs = ""
		
		for point in node.points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			xy_pairs += str(a_point["width"]) + "," + str(a_point["height"]) + ";"
			
		output["xyPairs"] = String(xy_pairs.rstrip(";"))
		
		return output
		
		
	def generatePolyline(self, node, macros={}):
		output = QtWidget("caPolyLine", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		
		output["polystyle"] = Enum("caPolyLine::Polyline")
		output["fillstyle"] = Enum("caPolyLine::Outline")
		
		xy_pairs = ""
		
		for point in node.points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			xy_pairs += str(a_point["width"]) + "," + str(a_point["height"]) + ";"
			
		output["xyPairs"] = String(xy_pairs.rstrip(";"))
		
		return output
	

	def generateImage(self, node, macros={}):
		output = QtWidget("caImage", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("filename", "file")
		
		return output
		
		
	def generateSlider(self, node, macros={}):
		output = QtWidget("caSlider", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		
		if output.pop("horizontal"):
			output["direction"] = Enum("Right")
		else:
			output["direction"] = Enum("Up")
		
		output["background"] = Color("$C4C4C4")
		output["borderWidth"] = Number(2)
		output["colorMode"] = Enum("caSlider::Alarm_Static")
		
		return output
		
	
	def generateScale(self, node, macros={}):
		output = QtWidget("caThermo", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		
		output["scalePosition"] = Enum("QwtThermoMarker::NoScale")
		
		if output.pop("horizontal"):
			output["direction"] = Enum("Right")
		else:
			output["direction"] = Enum("Up")
					
		return output
		

def generateQtFile(template, data, outputfile=""):
	a_display = QtDisplay()
	the_generator = QtGenerator()
	
	for key, item in template.items():
		if isinstance(item, Node):
			if item.classname == "Form":
				a_display.setProperties(item.attrs)
			else:
				data.update({
					"__parentx__" : a_display["geometry"]["x"],
					"__parenty__" : a_display["geometry"]["y"],
					"__parentwidth__" : a_display["geometry"]["width"],
					"__parentheight__" : a_display["geometry"]["height"]})
			
				a_display.place(item.apply(the_generator, data=data))

						
	a_display.writeQt(outputfile)
