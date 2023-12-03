import os
import re
import yaml

import pprint

from gestalt.Node import *
from gestalt.Type import *

##########################
#    Data Type Parsing   #
##########################

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

######################
#    Node Parsing    #
######################	

def read_node(typ, loader, node):
	params = loader.construct_mapping(node, deep=True)

	return Node(typ, layout=params)


def read_group_node(typ, loader, node):
	params = loader.construct_mapping(node, deep=True)

	children = params.pop("children", None)

	return GroupNode(typ, initial=children, layout=params)

def read_grid_node(loader, node):
	params = loader.construct_mapping(node, deep=True)

	children = params.pop("children", None)
	repeat_over = params.pop("repeat_over", None)
	padding = params.pop("padding", 0)
	ratio = params.pop("aspect_ratio", 1.0)

	return GridNode(initial=children, layout=params, repeat=repeat_over, padding=padding, ratio=ratio)

def read_flow_node(flow, loader, node):
	params = loader.construct_mapping(node, deep=True)

	children = params.pop("children", None)
	padding = params.pop("padding", 0)

	return FlowNode(initial=children, layout=params, padding=padding, flow=flow)

def read_repeat_node(flow, loader, node):
	params = loader.construct_mapping(node, deep=True)

	children = params.pop("children", None)
	repeat_over = params.pop("repeat_over", None)
	padding = params.pop("padding", 0)

	return RepeatNode(initial=children, layout=params, repeat=repeat_over, padding=padding, flow=flow)

def read_conditional_node(loader, node):	
	params = loader.construct_mapping(node, deep=True)

	children = params.pop("children", None)
	condition = params.pop("condition", None)

	return ConditionalNode(initial=children, layout=params, condition=condition)

def read_spacer_node(loader, node):
	params = loader.construct_mapping(node, deep=True)

	return SpacerNode(layout=params)

def read_stretch_node(flow, loader, node):
	params = loader.construct_mapping(node, deep=True)

	return StretchNode(flow=flow, subnode=next(iter(params.values())))

def read_center_node(flow, loader, node):
	params = loader.construct_mapping(node, deep=True)
	
	return CenterNode(flow=flow, subnode=next(iter(params.values())))


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
	
	"ActionButton", "Arc", "Array", "BooleanButton", "ByteMonitor",
	"CheckBox", "ChoiceButton", "ComboBox", "DataBrowser", "Ellipse",
	"EmbeddedDisplay", "FileSelector", "Group", "Image", "LED",
	"LEDMultiState", "Label", "Meter", "NavigationTabs", "Picture",
	"Polygon", "Polyline", "ProgressBar", "RadioButton", "Rectangle",
	"ScaledSlider", "Scrollbar", "SlideButton", "Spinner", "StripChart",
	"Symbol", "Table", "Tabs", "Tank", "TextEntry", "TextSymbol",
	"TextUpdate", "Thermometer", "ThreeDViewer", "WebBrowser", "XYPlot"
)

for widget_type in recognized_types:
	yaml.add_constructor("!" + widget_type, (lambda l, n, t=widget_type: read_node(t, l, n)), Loader=yaml.SafeLoader)
	
add_constructors("group", (lambda l, n: read_group_node("caFrame", l, n)))
	
add_constructors("grid", (lambda l, n: read_grid_node(l, n)))

add_constructors("conditional", (lambda l, n: read_conditional_node(l, n)))

add_constructors("spacer", (lambda l, n: read_spacer_node(l, n)))
	
add_constructors("flow", (lambda l, n: read_flow_node("vertical", l, n)))
add_constructors("vflow", (lambda l, n: read_flow_node("vertical", l, n)))
add_constructors("hflow", (lambda l, n: read_flow_node("horizontal", l, n)))
	
add_constructors("repeat", (lambda l, n: read_repeat_node("vertical", l, n)))
add_constructors("vrepeat", (lambda l, n: read_repeat_node("vertical", l, n)))
add_constructors("hrepeat", (lambda l, n: read_repeat_node("horizontal", l, n)))

add_constructors("stretch",  (lambda l, n: read_stretch_node("vertical", l, n)))
add_constructors("vstretch", (lambda l, n: read_stretch_node("vertical", l, n)))
add_constructors("hstretch", (lambda l, n: read_stretch_node("horizontal", l, n)))

add_constructors("center",  (lambda l, n: read_center_node("vertical", l, n)))
add_constructors("vcenter", (lambda l, n: read_center_node("vertical", l, n)))
add_constructors("hcenter", (lambda l, n: read_center_node("horizontal", l, n)))
	
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
