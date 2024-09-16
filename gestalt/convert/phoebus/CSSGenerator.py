import pathlib

from gestalt.Node import *
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from phoebusgen import screen

from gestalt.convert.phoebus.CSSWidget      import CSSWidget, reset_numbering
from gestalt.convert.phoebus.CSSGroup       import CSSGroup
from gestalt.convert.phoebus.CSSDisplay     import CSSDisplay
from gestalt.convert.phoebus.CSSTabbedGroup import CSSTabbedGroup
from gestalt.convert.phoebus.CSSAnonymous   import CSSAnonymous


class CSSGenerator(GestaltGenerator):
	def generateWidget(self, original, macros={}):
		return CSSWidget(original.classname, node=original, macros=macros)
		
	def generateGroup(self, original, macros={}):
		return CSSGroup(node=original, macros=macros)
		
	def generateAnonymousGroup(self, macros={}):
		return CSSAnonymous()
	
	def generateTabbedGroup(self, original, macros={}):
		return CSSTabbedGroup(node=original, macros=macros)
		
	def generateTextEntry(self, node, macros={}):
		return CSSWidget("TextEntry", node=node, macros=macros)
		
	def generateMenu(self, node, macros={}):
		return CSSWidget("ComboBox", node=node, macros=macros)
		
	def generateChoiceButton(self, node, macros={}):
		return CSSWidget("ChoiceButton", node=node, macros=macros)
		
		
	def generateRelatedDisplay(self, node, macros={}):
		output = CSSWidget("ActionButton", node=node, macros=macros)
		
		for item in node.links:
			_file = String(item.get("file", ""))
			_file.apply(macros)
			_file = _file.val()
			_file = str(_file).removesuffix( pathlib.PurePath(str(_file)).suffix ) + ".bob"
			
			
			_desc = String(item.get("label", ""))
			_desc.apply(macros)
			_desc = _desc.val()
			
			_args = String(item.get("macros", ""))
			_args.apply(macros)
			_args = _args.val().split(",")
			
			_rep = "window"
			
			if "replace" in item and item.replace:
				_rep = "replace"
			
			_macros = {}
			
			if _args[0]:
				for arg in _args:
					key, val = arg.split("=")
					_macros[key.strip()] = val.strip()
				
			output.widget.action_open_display(_file, _rep, description=_desc, macros=_macros)
				
		return output
		
		
	def generateShellCommand(self, node, macros={}):
		output = CSSWidget("ActionButton", node=node, macros=macros)
		
		for item in node.commands:
			_cmd = String(item.get("command", ""))
			_cmd.apply(macros)
			_cmd = _cmd.val()
			
			_desc = String(item.get("label", ""))
			_desc.apply(macros)
			_desc = _desc.val()
			
			output.widget.action_execute_command(_cmd, description=_desc)
				
		return output
		
		
	def generateMessageButton(self, node, macros={}):
		output = CSSWidget("ActionButton", node=node, macros=macros)
		
		output.widget.action_write_pv(str(output.pop("pv")), str(output.pop("value")))
		
		return output
		
		
	def generateText(self, node, macros={}):
		output = CSSWidget("Label", node=node, macros=macros)
		
		output.link("border", "border-color")
		output.link("border_width", "border-width")
		
		output["transparent"] = Bool(False)
		
		return output
	
		
	def generateTextMonitor(self, node, macros={}):
		output = CSSWidget("TextUpdate", node=node, macros=macros)
		
		output.link("border", "border-color")	
		output.link("border_width", "border-width")
		
		return output

		
	def generateLED(self, node, macros={}):
		output = CSSWidget("LEDMultiState", node=node, macros=macros)
		
		output.link("line", "border-color")
		
		falseval = output.pop("false-value")
		trueval  = output.pop("true-value")
		
		falsecol = output.pop("false-color")
		truecol  = output.pop("true-color")
		undefcol = output.pop("undefined-color")
		
		output.widget.state(falseval.val(), "", falsecol.val()["red"], falsecol.val()["green"], falsecol.val()["blue"], falsecol.val()["alpha"])
		output.widget.state(trueval.val(), "", truecol.val()["red"], truecol.val()["green"], truecol.val()["blue"], truecol.val()["alpha"])
		
		output.widget.fallback_label("")
		output.widget.fallback_color(undefcol.val()["red"], undefcol["green"], undefcol.val()["blue"], undefcol.val()["alpha"])
		
		return output

	
	def generateByteMonitor(self, node, macros={}):
		output = CSSWidget("ByteMonitor", node=node, macros=macros)
		
		output.link("on", "on-color")
		output.link("off", "off-color")
		output.link("startBit", "start-bit")
		output.link("numBits", "bits")
		
		output["square"] = Bool(True)
		
		return output
		
	
	def generateRectangle(self, node, macros={}):
		output = CSSWidget("Rectangle", node=node, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
			
		return output
		
		
	def generateEllipse(self, node, macros={}):
		output = CSSWidget("Ellipse", node=node, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
			
		return output
		
	
	def generateArc(self, node, macros={}):
		output = CSSWidget("Arc", node=node, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
		output.link("start_angle", "start-angle")
		output.link("total_angle", "span")
			
		return output
		
		
	def generatePolygon(self, node, macros={}):
		output = CSSWidget("Polygon", node=node, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
		
		my_points = List(node.points)
		my_points.apply(macros)
		
		for point in my_points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			output.widget.point(a_point["width"], a_point["height"])
		
		return output
		
		
	def generatePolyline(self, node, macros={}):
		output = CSSWidget("Polyline", node=node, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
		
		my_points = List(node.points)
		my_points.apply(macros)
		
		for point in my_points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			output.widget.point(a_point["width"], a_point["height"])
		
		return output
		
		
	def generateImage(self, node, macros={}):
		output = CSSWidget("Picture", node=node, macros=macros)
		
		output["stretch_image"] = Bool(True)
		
		return output
		
		
	def generateSlider(self, node, macros={}):
		output = CSSWidget("Scrollbar", node=node, macros=macros)
		
		return output

	
	def generateScale(self, node, macros={}):
		output = CSSWidget("Tank", node=node, macros=macros)
		
		output.link("empty", "background")
		output.link("fill", "foreground")
		
		output["scale_visible"] = Bool(False)
		
		return output
		

def generateCSSFile(template, data, outputfile=""):
	reset_numbering()
	
	a_display = CSSDisplay()
	the_generator = CSSGenerator()
	
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

						
	a_display.writeCSS(outputfile)
