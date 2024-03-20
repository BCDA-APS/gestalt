import os
import re
import yaml

import pprint

from gestalt.Node import *
from gestalt.Type import *

##########################
#    Data Type Parsing   #
##########################

my_templates = {}

def read_type(cls, loader, node):

	# Parse Dictionary
	try:
		params = loader.construct_mapping(node)
		return cls(params)
		
	except:
	
		# Parse Sequence 
		try:
			data = loader.construct_sequence(node)
			return cls(data)
			
		# Parse Scalar
		except:
			data = loader.construct_scalar(node)
			return cls(data)
			
			
def add_multi_constructors(typ_name, typ_func, regex=None):
	yaml.add_multi_constructor("!" + typ_name,              typ_func, Loader=yaml.SafeLoader)
	yaml.add_multi_constructor("!" + typ_name.lower(),      typ_func, Loader=yaml.SafeLoader)
	yaml.add_multi_constructor("!" + typ_name.upper(),      typ_func, Loader=yaml.SafeLoader)
	yaml.add_multi_constructor("!" + typ_name.capitalize(), typ_func, Loader=yaml.SafeLoader)
			
def add_constructors(typ_name, typ_func, regex=None):	
	yaml.add_constructor("!" + typ_name,              typ_func, Loader=yaml.SafeLoader)
	yaml.add_constructor("!" + typ_name.lower(),      typ_func, Loader=yaml.SafeLoader)
	yaml.add_constructor("!" + typ_name.upper(),      typ_func, Loader=yaml.SafeLoader)
	yaml.add_constructor("!" + typ_name.capitalize(), typ_func, Loader=yaml.SafeLoader)
			
	if regex:
		yaml.add_implicit_resolver(u"!" + typ_name, regex, Loader=yaml.SafeLoader)
			
add_constructors("string", (lambda l, n: read_type(String, l, n)))
add_constructors("number", (lambda l, n: read_type(Number, l, n)))
add_constructors("double", (lambda l, n: read_type(Double, l, n)))
add_constructors("bool",   (lambda l, n: read_type(Bool,   l, n)))
add_constructors("set",    (lambda l, n: read_type(Set,    l, n)), regex= re.compile(r'^[a-zA-Z0-9_:]+(\s*\|\s*[a-zA-Z0-9_:]+)+$'))
add_constructors("enum",   (lambda l, n: read_type(Enum,   l, n)), regex= re.compile(r'^\w+::\w+$'))
add_constructors("geom",   (lambda l, n: read_type(Rect,   l, n)), regex= re.compile(r'^-?\d+\s*(x\s*-?\d+\s*)+$'))
add_constructors("color",  (lambda l, n: read_type(Color,  l, n)), regex= re.compile(r'^\$([0-9A-Fa-f][0-9A-Fa-f])+$'))
add_constructors("font",   (lambda l, n: read_type(Font,   l, n)), regex= re.compile(r'^-[a-zA-Z][\w\s]*(-\s*[a-zA-Z][a-zA-Z_]+\s*)(-[0-9\s]+)$'))
add_constructors("align",  (lambda l, n: read_type(Alignment, l, n)), regex= re.compile(r'^TopLeft|TopMiddle|TopCenter|TopRight|MiddleLeft|MiddleMiddle|Middle|MiddleCenter|MiddleRight|CenterLeft|CenterMiddle|CenterCenter|Center|CenterRight|BottomLeft|BottomMiddle|BottomCenter|BottomRight$', re.IGNORECASE))
add_constructors("not",    (lambda l, n: read_type(Not,    l, n)))
		
######################
#    Node Parsing    #
######################	

def read_node(typ, loader, node):
	params = {}
	
	try:
		params = loader.construct_mapping(node, deep=True)
	except:
		pass

	return Node(typ, layout=params)

def read_group_node(typ, loader, node):
	params = loader.construct_mapping(node, deep=True)

	return GroupNode(typ, layout=params)


def read_special_node(node_type, loader, node, **kwargs):
	try:
		params = loader.construct_mapping(node, deep=True)
	except:
		pass

	return node_type(layout=params, **kwargs)


def read_template_multi(loader, suffix, node):
	try: 
		params = loader.construct_mapping(node, deep=True)
		my_templates[suffix] = next(iter(params.values()))
	except:
		params = loader.construct_sequence(node, deep=True)
		my_templates[suffix] = next(iter(params))
	
	return None
		
def read_apply_multi(loader, suffix, node):
	macros = {}
	
	try:
		macros = loader.construct_mapping(node, deep=True)
	except:
		pass
	
	return ApplyNode(macros=macros, subnode=my_templates.get(suffix, None))
	
def read_stretch_multi(loader, suffix, node, flow="vertical"):
	ret_node = yaml.SafeLoader.yaml_constructors["!" + suffix](loader, node)
	
	return StretchNode(flow=flow, subnode=ret_node)
	
def read_stretch_node(loader, node, flow="vertical"):
	try:
		params = loader.construct_mapping(node, deep=True)
		return StretchNode(flow=flow, subnode=next(iter(params.values())))
	except:
		params = loader.construct_sequence(node, deep=True)
		return StretchNode(flow=flow, subnode=next(iter(params)))

		
def read_center_multi(loader, suffix, node, flow="vertical"):
	ret_node = yaml.SafeLoader.yaml_constructors["!" + suffix](loader, node)
	
	return CenterNode(flow=flow, subnode=ret_node)
		
def read_center_node(loader, node, flow="vertical"):
	try:
		params = loader.construct_mapping(node, deep=True)
		return CenterNode(flow=flow, subnode=next(iter(params.values())))
	except:
		params = loader.construct_sequence(node, deep=True)
		return CenterNode(flow=flow, subnode=next(iter(params)))


recognized_types = (
	'caLabel', 'caLineEdit', 'caTextEntry', 'caMenu', 'caRelatedDisplay',
	'caNumeric', 'caApplyNumeric', 'caSlider', 'caChoice', 'caTextEntry',
	'caMessageButton', 'caToggleButton', 'caSpinbox', 'caByteController',
	'caLabelVertical', 'caGraphics', 'caPolyLine', 'caImage', 'caInclude',
	'caDoubleTabWidget', 'caClock', 'caLed', 'caLinearGauge', 'caMeter',
	'caCircularGauge', 'caMultiLineString', 'caThermo', 'caCartesianPlot',
	'caStripPlot', 'caByte', 'caTable', 'caWaveTable', 'caBitnames',
	'caCamera', 'caCalc', 'caWaterfallPlot', 'caScan2D', 'caLineDraw',
	'caShellCommand', 'caScriptButton', 'caMimeDisplay', 'Form',
	
	"ActionButton", "Array", "BooleanButton", "CheckBox", "ComboBox", 
	"DataBrowser", "EmbeddedDisplay", "FileSelector", "Label",
	"LEDMultiState", "NavigationTabs", "Picture", "ProgressBar", 
	"RadioButton", "ScaledSlider", "Scrollbar", "SlideButton", "Spinner", 
	"StripChart", "Symbol", "Table", "Tabs", "Tank", "TextSymbol", 
	"TextUpdate", "Thermometer", "ThreeDViewer", "WebBrowser", "XYPlot"
)

for widget_type in recognized_types:
	yaml.add_constructor("!" + widget_type, (lambda l, n, t=widget_type: read_node(t, l, n)), Loader=yaml.SafeLoader)
	
add_constructors("group", (lambda l, n: read_group_node("caFrame", l, n)))
	
add_constructors("grid", (lambda l, n: read_special_node(GridNode, l, n)))

add_constructors("conditional", (lambda l, n: read_special_node(ConditionalNode, l, n)))
add_multi_constructors("template", read_template_multi)
add_multi_constructors("apply",   read_apply_multi)

add_constructors("spacer", (lambda l, n: read_special_node(SpacerNode, l, n)))
	
add_constructors("flow",  (lambda l, n: read_special_node(FlowNode, l, n, flow="vertical")))
add_constructors("vflow", (lambda l, n: read_special_node(FlowNode, l, n, flow="vertical")))
add_constructors("hflow", (lambda l, n: read_special_node(FlowNode, l, n, flow="horizontal")))
	
add_constructors("repeat",  (lambda l, n: read_special_node(RepeatNode, l, n,  flow="vertical")))
add_constructors("vrepeat", (lambda l, n: read_special_node(RepeatNode, l, n,  flow="vertical")))
add_constructors("hrepeat", (lambda l, n: read_special_node(RepeatNode, l, n,  flow="horizontal")))

add_multi_constructors("stretch:",  (lambda l, s, n: read_stretch_multi(l, s, n, flow="vertical")))
add_multi_constructors("vstretch:", (lambda l, s, n: read_stretch_multi(l, s, n, flow="vertical")))
add_multi_constructors("hstretch:", (lambda l, s, n: read_stretch_multi(l, s, n, flow="horizontal")))

add_constructors("stretch",  (lambda l, n: read_stretch_node(l, n, flow="vertical")))
add_constructors("vstretch", (lambda l, n: read_stretch_node(l, n, flow="vertical")))
add_constructors("hstretch", (lambda l, n: read_stretch_node(l, n, flow="horizontal")))


add_multi_constructors("center:",  (lambda l, s, n: read_center_multi(l, s, n, flow="vertical")))
add_multi_constructors("vcenter:", (lambda l, s, n: read_center_multi(l, s, n, flow="vertical")))
add_multi_constructors("hcenter:", (lambda l, s, n: read_center_multi(l, s, n, flow="horizontal")))

add_constructors("center",  (lambda l, n: read_center_node(l, n, flow="vertical")))
add_constructors("vcenter", (lambda l, n: read_center_node(l, n, flow="vertical")))
add_constructors("hcenter", (lambda l, n: read_center_node(l, n, flow="horizontal")))
	
add_constructors("ShellCommand",   (lambda l, n: read_special_node(ShellCommandNode, l, n)))
add_constructors("RelatedDisplay", (lambda l, n: read_special_node(RelatedDisplayNode, l, n)))
add_constructors("MessageButton",  (lambda l, n: read_special_node(MessageButtonNode, l, n)))
add_constructors("Text",           (lambda l, n: read_special_node(TextNode, l, n)))
add_constructors("TextEntry",      (lambda l, n: read_special_node(TextEntryNode, l, n)))
add_constructors("TextMonitor",    (lambda l, n: read_special_node(TextMonitorNode, l, n)))
add_constructors("Menu",           (lambda l, n: read_special_node(MenuNode, l, n)))
add_constructors("ChoiceButton",   (lambda l, n: read_special_node(ChoiceButtonNode, l, n)))
add_constructors("LED",            (lambda l, n: read_special_node(LEDNode, l, n)))
add_constructors("ByteMonitor",    (lambda l, n: read_special_node(ByteMonitorNode, l, n)))
add_constructors("Rectangle",      (lambda l, n: read_special_node(RectangleNode, l, n)))
add_constructors("Ellipse",        (lambda l, n: read_special_node(EllipseNode, l, n)))
add_constructors("Arc",            (lambda l, n: read_special_node(ArcNode, l, n)))
add_constructors("Image",          (lambda l, n: read_special_node(ImageNode, l, n)))
add_constructors("Polygon",        (lambda l, n: read_special_node(PolygonNode, l, n)))
add_constructors("PolyLine",       (lambda l, n: read_special_node(PolylineNode, l, n)))
add_constructors("Slider",         (lambda l, n: read_special_node(SliderNode, l, n)))
add_constructors("Scale",          (lambda l, n: read_special_node(ScaleNode, l, n)))
	
#####################
#   Include Files   #
#####################

include_regex = re.compile(r'^#include\s*(.*)$')

def read_file(filename, includes_locations, included_files):
	the_data_out = ""
	
	with open (filename) as the_file:
		the_data_in = the_file.readlines()
		
		for line in the_data_in:
			check = include_regex.match(line)
			
			if check:
				include_file = check.group(1).strip()
				include_file_path = ""
				
				for check_dir in includes_locations:
					
					test_path = os.path.abspath(check_dir + "/" + include_file)
						
					if os.path.exists(test_path):
						include_file_path = test_path
						break
					
				
				if include_file_path == "":
					print( "Include file does not exist in path (" + include_file + ")")
					continue
				
				
				if include_file not in included_files:
					included_files.append(include_file)
					the_data_out += read_file(include_file_path, includes_locations, included_files)
					
			else:
				the_data_out += line
				
	return the_data_out
	
	
	
def parse(filename, includes_dirs):
	return yaml.safe_load(read_file(filename, includes_dirs, []))
