import ast

from gestalt.nodes.Node import Node
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from gestalt.convert.qt.QtWidget  import QtWidget, reset_numbering
from gestalt.convert.qt.QtGroup   import QtGroup
from gestalt.convert.qt.QtDisplay import QtDisplay
from gestalt.convert.qt.QtTabbedGroup    import QtTabbedGroup
from gestalt.convert.qt.QtRelatedDisplay import QtRelatedDisplay
from gestalt.convert.qt.QtShellCommand   import QtShellCommand
from gestalt.convert.qt.QtMessageButton  import QtMessageButton
from gestalt.convert.qt.QtAnonymous      import QtAnonymous
from gestalt.convert.qt.QtLED            import QtLED

format_conversion = {
	"String"      : Enum("caLineEdit::string"),
	"Decimal"     : Enum("caLineEdit::decimal"),
	"Engineering" : Enum("caLineEdit::engr_notation"),
	"Exponential" : Enum("caLineEdit::exponential"),
	"Compact"     : Enum("caLineEdit::compact"),
	"Hexadecimal" : Enum("caLineEdit::hexadecimal"),
	"Binary"      : Enum("caLineEdit::octal")
}

border_conversion = {
	"Solid"       : Enum("caGraphics::Solid"),
	"Dashed"      : Enum("caGraphics::Dash"),
}

line_conversion = {
	"Solid"       : Enum("caPolyLine::Solid"),
	"Dashed"      : Enum("caPolyLine::Dash"),
}

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
		
		output["fontScaleMode"] = Enum("ESimpleLabel::Height")
		
		return output
		
		
	def generateTextEntry(self, node, macros={}):
		output = QtWidget("caTextEntry", node=node, macros=macros)
		
		output.link("channel", "pv")
		output.link("formatType", "format", conversion=format_conversion)
		
		output["colorMode"]     = Enum("caLineEdit::Static")
		output["fontScaleMode"] = Enum("caLineEdit::Height")
		
		return output
		
		
	def generateTextMonitor(self, node, macros={}):
		output = QtWidget("caLineEdit", node=node, macros=macros)
		
		output.link("channel",        "pv")
		output.link("frameColor",     "border-color")
		output.link("frameLineWidth", "border-width")
		output.link("formatType",     "format", conversion=format_conversion)
		
		output["colorMode"]     = Enum("caLineEdit::Static")
		output["fontScaleMode"] = Enum("caLineEdit::Height")
		
		return output
		
		
	def generateMenu(self, node, macros={}):
		output = QtWidget("caMenu", node=node, macros=macros)
		
		output.link("channel", "pv")
			
		output["colorMode"]     = Enum("caMenu::Static")
		output["elevation"]     = Enum("caMenu::as_is")
		
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
		output.link("linestyle",  "border-style", conversion=border_conversion)
		
		output["form"] = Enum("caGraphics::Rectangle")
		output["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		
	
	def generateEllipse(self, node, macros={}):
		output = QtWidget("caGraphics", node=node, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		output.link("linestyle",  "border-style", conversion=border_conversion)
		
		output["form"] = Enum("caGraphics::Circle")
		output["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		
		
	def generateArc(self, node, macros={}):
		output = QtWidget("caGraphics", node=node, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		output.link("linestyle",  "border-style", conversion=border_conversion)
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
		output.link("linestyle",  "border-style", conversion=line_conversion)
		
		output["polystyle"] = Enum("caPolyLine::Polygon")
		output["fillstyle"] = Enum("caPolyLine::Filled")
		
		xy_pairs = ""
		
		my_points = List(node.points)
		my_points.apply(macros)
		
		for point in my_points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			xy_pairs += str(a_point["width"]) + "," + str(a_point["height"]) + ";"
			
		output["xyPairs"] = String(xy_pairs.rstrip(";"))
		
		return output
		
		
	def generatePolyline(self, node, macros={}):
		output = QtWidget("caPolyLine", node=node, macros=macros)
		
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		output.link("linestyle",  "border-style", conversion=line_conversion)
		
		output["polystyle"] = Enum("caPolyLine::Polyline")
		output["fillstyle"] = Enum("caPolyLine::Outline")
		
		xy_pairs = ""
		
		my_points = List(node.points)
		my_points.apply(macros)
				
		for point in my_points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			xy_pairs += str(a_point["width"]) + "," + str(a_point["height"]) + ";"
			
		output["xyPairs"] = String(xy_pairs.rstrip(";"))
		
		return output
	

	def generateImage(self, node, macros={}):
		output = QtWidget("caImage", node=node, macros=macros)
		
		output.link("filename", "file")
		
		return output
		
	def generateInclude(self, node, macros={}):
		output = QtWidget("caInclude", node=node, macros=macros)
		
		output["file"] = str(output["file"]) + ".ui"
		output.link("filename", "file")
		output.link("macro", "macros")
		
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

	def generateCalc(self, node, macros={}):
		output = QtWidget("caCalc", node=node, macros=macros)
		
		output.link("variable", "pv")
		output.link("channel",  "A")
		output.link("channelB", "B")
		output.link("channelC", "C")
		output.link("channelD", "D")
		
		equation = str(output.pop("calc"))
		
		def evalNode(node):
			if isinstance(node, ast.Expression):
				return evalNode(node.body)
				
			elif isinstance(node, ast.Constant):
				return str(node.value)
				
			elif isinstance(node, ast.Name):
				return node.id
				
			elif isinstance(node, ast.Compare):
				output = "(" + evalNode(node.left)
				ops_check = { 
					ast.Eq: "=",
					ast.NotEq: "#",
					ast.Lt: "<",
					ast.LtE: "<=",
					ast.Gt: ">",
					ast.GtE: ">=",
					ast.Is: "=",
					ast.IsNot: "#"
				}
				
				for i in range(len(node.ops)):
					output += ops_check[type(node.ops[i])]
					output += evalNode(node.comparators[i])
					
				return output + ")"
				
			elif isinstance(node, ast.BoolOp):
				output = "(" + evalNode(node.values[0])
				
				for i in range(len(node.values) - 1):
					if isinstance(node.op, ast.And):
						output += "&&"
					elif isinstance(node.op, ast.Or):
						output += "||"
					
					output += evalNode(node.values[i+1])
				
				return output + ")"
				
			elif isinstance(node, ast.BinOp):
				ops_check = {
					ast.Add:  "+",
					ast.Sub:  "-",
					ast.Mult: "*",
					ast.Div:  "/",
					ast.Pow:  "^",
					ast.BitOr: "|",
					ast.BitAnd: "&",
					ast.BitXor: " XOR ",
					ast.LShift: "<<",
					ast.RShift: ">>"
				}
				
				return "(" + evalNode(node.left) + ops_check[type(node.op)] + evalNode(node.right) + ")"
					
			elif isinstance(node, ast.UnaryOp):
				if isinstance(node.op, ast.Not):
					return "!(" + evalNode(node.operand) + ")"
				elif isinstance(node.op, ast.Invert):
					return "~" + evalNode(node.operand)
				elif isinstance(node.op, ast.USub):
					return "-" + evalNode(node.operand)
			else:
				print(ast.dump(node, indent=4))

		output["calc"] = String(evalNode(ast.parse(equation, mode="eval")))
				
		output["foreground"] = Color("$00000000")
		output["background"] = Color("$00000000")
		output["eventSignal"] = Enum("caCalc::onAnyChange")
		
		return output
		
	
def generateQtFile(template, data, outputfile=""):
	reset_numbering()
	
	a_display = QtDisplay()
	the_generator = QtGenerator()
	
	for key, item in template.items():
		if isinstance(item, Node):
			item.name = key
			
			if item.classname == "Form":
				for key, val in item.properties["attrs"].items():
					a_display.setProperty(key, val)
				a_display.updateProperties(data)
			else:
				applier = item.apply(the_generator)
				
				while True:
					a_display.updateMacros(a_display, data)
										
					try:
						next(applier)
						a_display.place(applier.send(data))
					except StopIteration:
						break
						
	a_display.writeQt(outputfile)

