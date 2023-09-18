import os
import re
import yaml

from gestalt.Type import *
from gestalt.Gestalt import Node, GroupNode, RepeatNode, StretchNode, CenterNode

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
			
			
yaml.add_constructor("!string", (lambda l, n: read_type(String, l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!number", (lambda l, n: read_type(Number, l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!double", (lambda l, n: read_type(Double, l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!bool",   (lambda l, n: read_type(Bool,   l, n)), Loader=yaml.SafeLoader)

set_regex = re.compile(r'^[a-zA-Z0-9_:]+(\s*\|\s*[a-zA-Z0-9_:]+)+$')
yaml.add_constructor("!set",    (lambda l, n: read_type(Set, l, n)),    Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!set", set_regex, Loader=yaml.SafeLoader)
			
enum_regex = re.compile(r'^\w+::\w+$')
yaml.add_constructor("!enum", (lambda l, n: read_type(Enum, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!enum", enum_regex, Loader=yaml.SafeLoader)
			
rect_regex = re.compile(r'^-?\d+\s*(x\s*-?\d+\s*)+$')
yaml.add_constructor("!geom", (lambda l, n: read_type(Rect, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!geom", rect_regex, Loader=yaml.SafeLoader)

color_regex = re.compile(r'^\$([0-9A-Fa-f][0-9A-Fa-f])+$')
yaml.add_constructor("!color", (lambda l, n: read_type(Color, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver(u'!color', color_regex, Loader=yaml.SafeLoader)



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


def read_repeat_node(flow, loader, node):
	params = loader.construct_mapping(node, deep=True)

	children = params.pop("children", None)
	repeat_over = params.pop("repeat_over", None)
	padding = params.pop("padding", 0)

	return RepeatNode(initial=children, layout=params, repeat=repeat_over, padding=padding, flow=flow)

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
	'caShellCommand', 'caScriptButton', 'caMimeDisplay', 'Form'
)

for widget_type in recognized_types:
	yaml.add_constructor("!" + widget_type, (lambda l, n, t=widget_type: read_node(t, l, n)), Loader=yaml.SafeLoader)
	
yaml.add_constructor("!group", (lambda l, n: read_group_node("caFrame", l, n)), Loader=yaml.SafeLoader)

yaml.add_constructor("!repeat", (lambda l, n: read_repeat_node("vertical", l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!vrepeat", (lambda l, n: read_repeat_node("vertical", l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!hrepeat", (lambda l, n: read_repeat_node("horizontal", l, n)), Loader=yaml.SafeLoader)

yaml.add_constructor("!stretch",  (lambda l, n: read_stretch_node("vertical", l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!vstretch", (lambda l, n: read_stretch_node("vertical", l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!hstretch", (lambda l, n: read_stretch_node("horizontal", l, n)), Loader=yaml.SafeLoader)

yaml.add_constructor("!center",  (lambda l, n: read_center_node("vertical", l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!vcenter", (lambda l, n: read_center_node("vertical", l, n)), Loader=yaml.SafeLoader)
yaml.add_constructor("!hcenter", (lambda l, n: read_center_node("horizontal", l, n)), Loader=yaml.SafeLoader)
	
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
	
