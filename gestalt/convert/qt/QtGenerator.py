from gestalt.Node import *
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from gestalt.convert.qt.QtWidget  import QtWidget
from gestalt.convert.qt.QtGroup   import QtGroup
from gestalt.convert.qt.QtDisplay import QtDisplay
from gestalt.convert.qt.QtTabbedGroup    import QtTabbedGroup
from gestalt.convert.qt.QtRelatedDisplay import QtRelatedDisplay
from gestalt.convert.qt.QtShellCommand   import QtShellCommand
from gestalt.convert.qt.QtMessageButton  import QtMessageButton
from gestalt.convert.qt.QtAnonymous      import QtAnonymous
from gestalt.convert.qt.QtLED            import QtLED

class QtGenerator(GestaltGenerator):
	def generateWidget(self, original, macros={}):
		return QtWidget(original.classname, node=original, macros=macros)
		
	def generateGroup(self, original, macros={}):
		return QtGroup(node=original, macros=macros)
	
	def generateAnonymousGroup(self, macros={}):
		return QtAnonymous()
		
	def generateTabbedGroup(self, original, macros={}):
		return QtTabbedGroup(node=original, macros=macros)
		
	def generateRelatedDisplay(self, node, macros={}):
		return QtRelatedDisplay(node=node, macros=macros)
		
	def generateShellCommand(self, node, macros={}):
		return QtShellCommand(node=node, macros=macros)
		
	def generateMessageButton(self, node, macros={}):
		return QtMessageButton(node=node, macros=macros)
		
	def generateLED(self, node, macros={}):
		return QtLED(node=node, macros=macros)
		
	def generateText(self, node, macros={}):
		output = QtWidget("caLabel", node=node, macros=macros)
		
		output.link("borderColor", "border-color")
		output.link("borderWidth", "border-width")
		
		output["fontScaleMode"] = Enum("ESimpleLabel::None")
		
		return output
		
		
	def generateTextEntry(self, node, macros={}):
		output = QtWidget("caTextEntry", node=node, macros=macros)
		
		output.link("channel", "pv")
			
		output["colorMode"]     = Enum("caLineEdit::Static")
		output["fontScaleMode"] = Enum("caLineEdit::None")
		
		return output
		
		
	def generateTextMonitor(self, node, macros={}):
		output = QtWidget("caLineEdit", node=node, macros=macros)
		
		output.link("channel", "pv")
		output.link("frameColor", "border-color")
		output.link("frameLineWidth", "border-width")
			
		output["colorMode"]     = Enum("caLineEdit::Static")
		output["fontScaleMode"] = Enum("caLineEdit::None")
		
		return output
		
		
	def generateMenu(self, node, macros={}):
		output = QtWidget("caMenu", node=node, macros=macros)
		
		output.link("channel", "pv")
			
		output["colorMode"] = Enum("caMenu::Static")
		
		return output
		
		
	def generateChoiceButton(self, node, macros={}):
		output = QtWidget("caChoice", node=node, macros=macros)
		
		output.link("channel", "pv")
		output.link("bordercolor", "selected")
		
		if output.pop("horizontal"):
			output["stackingMode"] = Enum("Column")
		else:
			output["stackingMode"] = Enum("Row")
			
		output["colorMode"] = Enum("caChoice::Static")
		
		return output
		
		
	def generateByteMonitor(self, node, macros={}):
		output = QtWidget("caByteController", node=node, macros=macros)
		
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
		output = QtWidget("caGraphics", node=node, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		
		output["form"] = Enum("caGraphics::Rectangle")
		output["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		
	
	def generateEllipse(self, node, macros={}):
		output = QtWidget("caGraphics", node=node, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		
		output["form"] = Enum("caGraphics::Circle")
		output["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		
		
	def generateArc(self, node, macros={}):
		output = QtWidget("caGraphics", node=node, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		output.link("startAngle", "start-angle")
		output.link("spanAngle",  "span")
		
		output["form"] = Enum("caGraphics::Arc")
		output["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		
	
	def generatePolygon(self, node, macros={}):
		output = QtWidget("caPolyLine", node=node, macros=macros)
		
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
		output = QtWidget("caPolyLine", node=node, macros=macros)
		
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
		output = QtWidget("caImage", node=node, macros=macros)
		
		output.link("filename", "file")
		
		return output
		
		
	def generateSlider(self, node, macros={}):
		output = QtWidget("caSlider", node=node, macros=macros)
		
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
		output = QtWidget("caThermo", node=node, macros=macros)
		
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
				for key, val in item.properties["attrs"].items():
					a_display.setProperty(key, val)
				a_display.updateProperties(data)
			else:
				data.update({
					"__parentx__" : a_display["geometry"]["x"],
					"__parenty__" : a_display["geometry"]["y"],
					"__parentwidth__" : a_display["geometry"]["width"],
					"__parentheight__" : a_display["geometry"]["height"]})
			
				a_display.place(item.apply(the_generator, data=data))

						
	a_display.writeQt(outputfile)
