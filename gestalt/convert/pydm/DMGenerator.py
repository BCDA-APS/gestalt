import ast
import pathlib

from gestalt.Node import *
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from gestalt.convert.pydm.DMWidget  import DMWidget, reset_numbering
from gestalt.convert.pydm.DMGroup   import DMGroup
from gestalt.convert.pydm.DMDisplay import DMDisplay
from gestalt.convert.pydm.DMTabbedGroup    import DMTabbedGroup
from gestalt.convert.pydm.DMAnonymous      import DMAnonymous

from gestalt.convert.pydm.DMTypes      import *
from gestalt.convert.pydm.StyleWriters import *

label_conversion = {
	"String"      : Enum("PyDMLabel::String"),
	"Decimal"     : Enum("PyDMLabel::Decimal"),
	"Engineering" : Enum("PyDMLabel::Default"),
	"Exponential" : Enum("PyDMLabel::Exponential"),
	"Compact"     : Enum("PyDMLabel::Default"),
	"Hexadecimal" : Enum("PyDMLabel::Hex"),
	"Binary"      : Enum("PyDMLabel::Binary")
}

edit_conversion = {
	"String"      : Enum("PyDMLineEdit::String"),
	"Decimal"     : Enum("PyDMLineEdit::Decimal"),
	"Engineering" : Enum("PyDMLineEdit::Default"),
	"Exponential" : Enum("PyDMLineEdit::Exponential"),
	"Compact"     : Enum("PyDMLineEdit::Default"),
	"Hexadecimal" : Enum("PyDMLineEdit::Hex"),
	"Binary"      : Enum("PyDMLineEdit::Binary")
}

border_conversion = {
	"Solid"       : Enum("Qt::SolidLine"),
	"Dashed"      : Enum("Qt::DashLine")
}

class DMGenerator(GestaltGenerator):
	def generateWidget(self, original, macros={}):
		return DMWidget(original.classname, node=original, macros=macros)
		
	def generateGroup(self, original, macros={}):
		return DMGroup(node=original, macros=macros)
	
	def generateAnonymousGroup(self, macros={}):
		return DMAnonymous()
		
	def generateTabbedGroup(self, original, macros={}):
		return DMTabbedGroup(node=original, macros=macros)
		
	def generateRelatedDisplay(self, node, macros={}):
		output = DMWidget("PyDMRelatedDisplayButton", node=node, macros=macros)
		
		output["showIcon"] = Bool(False)
		output["openInNewWindow"] = Bool(True)
		
		output.addStyleWriter(write_font)
		output.addStyleWriter(write_color)
		output.addStyleWriter(style_button)
		
		links = String(node.links)
		links.apply(macros)
		
		labels = []
		files = []
		args = []
		
		for item in List(links):
			a_label = String(item.get("label", ""))
			a_label.apply(macros)

			a_file = String(item.get("file", ""))
			a_file.apply(macros)
			a_file = str(a_file).removesuffix( pathlib.PurePath(str(a_file)).suffix ) + ".ui"
			
			a_macro = String(item.get("macros", ""))
			a_macro.apply(macros)
			
			labels.append(str(a_label))
			files.append(str(a_file))
			args.append(str(a_macro))
			
		output["titles"] = List(labels)
		output["filenames"] = List(files)
		output["macros"] = List(args)
		
		return output
		
	def generateShellCommand(self, node, macros={}):
		output = DMWidget("PyDMShellCommand", node=node, macros=macros)
		
		the_list = String(node.commands)
		the_list.apply(macros)
		
		labels = []
		commands = []
		
		for item in List(the_list):
			labels.append(str(item.get("label", "")))
			commands.append(str(item.get("command", "")))
		
		output["titles"] = List(labels)
		output["commands"] = List(commands)
		
		output["showIcon"] = Bool(False)
		output["stdout"] = Enum("PyDMShellCommand::SHOW")
			
		output.addStyleWriter(write_font)
		output.addStyleWriter(write_color)
		
		return output
		
	def generateLED(self, node, macros={}):
		output = DMWidget("PyDMMultiStateIndicator", node=node, macros=macros)
		
		output.link("renderAsRectangle", "square")
		
		output.link("state0Color", "undefined-color")
		output.link("state1Color", "false-color")
		output.link("state2Color", "true-color")
		
		fcheck = "(var==" + str(int(output.pop("false-value"))) + ")"
		tcheck = "(var==" + str(int(output.pop("true-value"))) + ")"
		
		expression = "1*" + fcheck + "+2*" + tcheck

		channel = "calc://" + output.name + "?var=ca://" + str(output.pop("pv")) + "?expr=" + expression
		
		output.pop("border-color")
	
		return output
		
	def generateText(self, node, macros={}):
		output = DMWidget("PyDMLabel", node=node, macros=macros)
		
		output.addStyleWriter(write_frameborder)
		output.addStyleWriter(write_color)
		
		return output
		
		
	def generateTextEntry(self, node, macros={}):
		output = DMWidget("PyDMLineEdit", node=node, macros=macros)
		
		output.addStyleWriter(style_textentry)
		output.addStyleWriter(write_color)
		
		output.link("channel", "pv")
		output.link("displayFormat", "format", conversion=edit_conversion)
		
		return output
		
		
	def generateTextMonitor(self, node, macros={}):
		output = DMWidget("PyDMLabel", node=node, macros=macros)
		
		output.addStyleWriter(write_frameborder)
		output.addStyleWriter(write_color)
		
		output.link("channel",        "pv")
		output.link("displayFormat",  "format", conversion=label_conversion)
		
		return output
		
		
	def generateMenu(self, node, macros={}):
		output = DMWidget("PyDMEnumComboBox", node=node, macros=macros)
		
		output.link("channel", "pv")

		return output
		
		
	def generateMessageButton(self, node, macros={}):
		output = DMWidget("PyDMPushButton", node=node, macros=macros)
		
		output.link("channel", "pv")
		output.link("pressValue", "value")
		
		output.addStyleWriter(write_font)
		output.addStyleWriter(write_color)
		output.addStyleWriter(style_button)
		
		return output
		
		
	def generateChoiceButton(self, node, macros={}):
		output = DMWidget("PyDMEnumButton", node=node, macros=macros)
		
		output.link("channel", "pv")
		
		if output.pop("horizontal"):
			output["orientation"] = Enum("Qt::Horizontal")
		else:
			output["orientation"] = Enum("Qt::Vertical")
		
		return output
		
		
	def generateByteMonitor(self, node, macros={}):
		output = DMWidget("PyDMByteIndicator", node=node, macros=macros)
		
		output.link("channel", "pv")
		output.link("shift", "start-bit")
		output.link("numBits", "bits")
		output.link("offColor", "off-color")
		output.link("onColor", "on-color")
		
		if output.pop("horizontal"):
			output["orientation"] = Enum("Qt::Horizontal")
		else:
			output["orientation"] = Enum("Qt::Vertical")
		
		return output
		
		
	def generateRectangle(self, node, macros={}):
		output = DMWidget("PyDMDrawingRectangle", node=node, macros=macros)
		
		output["brush"] = Brush(output.pop("background"))
		
		output.link("penWidth",  "border-width")
		output.link("penColor",  "border-color")
		output.link("penStyle",  "border-style", conversion=border_conversion)
		
		return output
		
	
	def generateEllipse(self, node, macros={}):
		output = DMWidget("PyDMDrawingEllipse", node=node, macros=macros)
		
		output["brush"] = Brush(output.pop("background"))
		
		output.link("penWidth",   "border-width")
		output.link("penColor",  "border-color")
		output.link("penStyle",  "border-style", conversion=border_conversion)
		
		return output
		
		
	def generateArc(self, node, macros={}):
		output = DMWidget("PyDMDrawingChord", node=node, macros=macros)
		
		output["brush"] = Brush(output.pop("background"))
		
		output.link("penWidth",   "border-width")
		output.link("penColor",  "border-color")
		output.link("penStyle",  "border-style", conversion=border_conversion)
		output.link("startAngle", "start-angle")
		output.link("spanAngle",  "span")
		
		return output
		
	
	def generatePolygon(self, node, macros={}):
		output = DMWidget("PyDMDrawingIrregularPolygon", node=node, macros=macros)
		
		output["brush"] = Brush(output.pop("background"))
		
		output.link("penWidth",   "border-width")
		output.link("penColor",  "border-color")
		output.link("penStyle",  "border-style", conversion=border_conversion)
		
		xy_pairs = []
		
		my_points = List(node.points)
		my_points.apply(macros)
		
		for point in my_points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			xy_pairs.append(str(a_point["width"]) + "," + str(a_point["height"]))
			
		output["points"] = List(xy_pairs)
		
		return output
		
		
	def generatePolyline(self, node, macros={}):
		output = DMWidget("PyDMDrawingPolyline", node=node, macros=macros)
		
		output.link("penWidth",   "border-width")
		output.link("penColor",  "border-color")
		output.link("penStyle",  "border-style", conversion=border_conversion)
				
		xy_pairs = []
		
		my_points = List(node.points)
		my_points.apply(macros)
				
		for point in my_points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			xy_pairs.append(str(a_point["width"]) + "," + str(a_point["height"]))
			
		output["points"] = List(xy_pairs)
		
		return output
	

	def generateImage(self, node, macros={}):
		output = DMWidget("PyDMDrawingImage", node=node, macros=macros)
		
		output.link("filename", "file")
		
		output["aspectRatioMode"] = Enum("Qt::IgnoreAspectRatio")
		
		return output
		
		
	def generateSlider(self, node, macros={}):
		output = DMWidget("PyDMSlider", node=node, macros=macros)
		
		output.link("channel", "pv")
		
		if output.pop("horizontal"):
			output["orientation"] = Enum("Qt::Horizontal")
		else:
			output["orientation"] = Enum("Qt::Vertical")
		
		return output
		
	
	def generateScale(self, node, macros={}):
		output = DMWidget("PyDMAnalogIndicator", node=node, macros=macros)
		
		output.link("channel", "pv")
		output.link("backgroundColor", "background")
		output.link("indicatorColor",  "foreground")
		
		if output.pop("horizontal"):
			output["orientation"] = Enum("Qt::Horizontal")
		else:
			output["orientation"] = Enum("Qt::Vertical")
		
		output["flipScale"] = Bool(True)
		output["showValue"] = Bool(False)
			
		return output

	def generateCalc(self, node, macros={}):
		return None
		
		output = DMWidget("PyDMLabel", node=node, macros=macros)
		
		output.addStyleWriter(write_frameborder)
		output.addStyleWriter(write_color)
		
		pvname = str(output.pop("pv"))
		
		name = "calc://pv_" + pvname
		add_local_pv(pvname)
		
		equation = str(output.pop("calc"))
		calc = ""
		
		def evalNode(node):			
			if isinstance(node, ast.Expression):
				return evalNode(node.body)
				
			elif isinstance(node, ast.Constant):
				return str(node.value)
				
			elif isinstance(node, ast.Name):
				return str(node.id)
				
			elif isinstance(node, ast.Compare):
				output = "(" + evalNode(node.left)
				ops_check = { 
					ast.Eq: "==",
					ast.NotEq: "!=",
					ast.Lt: "<",
					ast.LtE: "<=",
					ast.Gt: ">",
					ast.GtE: ">=",
					ast.Is: "==",
					ast.IsNot: "!="
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
				if isinstance(node.op, ast.Pow):
					return "pow(" + evalNode(node.left) + "," + evalNode(node.right) + ")"
				else:
					ops_check = {
						ast.Add:  "+",
						ast.Sub:  "-",
						ast.Mult: "*",
						ast.Div:  "/",
						ast.BitOr: "|",
						ast.BitAnd: "&",
						ast.BitXor: "^",
						ast.LShift: "<<",
						ast.RShift: ">>"
					}
					
					return evalNode(node.left) + ops_check[type(node.op)] + evalNode(node.right)
					
			elif isinstance(node, ast.UnaryOp):
				if isinstance(node.op, ast.Not):
					return "not(" + evalNode(node.operand) + ")"
				elif isinstance(node.op, ast.Invert):
					return "~(" + evalNode(node.operand) + ")"
				elif isinstance(node.op, ast.USub):
					return "-" + evalNode(node.operand)
			else:
				print(ast.dump(node, indent=4))
				
			
			calc += evalNode(ast.parse(equation, mode="eval"))
		
			full = name + "?A={A}&B={B}&C={C}&D={D}&expr=" + calc
			
			output["channel"] = full.format(
				A = get_pv(str(output.pop("A"))), 
				B = get_pv(str(output.pop("B"))), 
				C = get_pv(str(output.pop("C"))), 
				D = get_pv(str(output.pop("D")))
			)
			
			return output
		
		
		
	
def generateDMFile(template, data, outputfile=""):
	reset_numbering()
	
	a_display = DMDisplay()
	the_generator = DMGenerator()
	
	for key, item in template.items():
		if isinstance(item, Node):
			item.name = key
			
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

						
	a_display.writeDM(outputfile)

