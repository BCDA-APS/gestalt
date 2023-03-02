import re
import yaml

from gestalt.Type import *
from gestalt.Gestalt import Node

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
			
rect_regex = re.compile(r'^\d+\s*(x\s*\d+\s*)+$')
yaml.add_constructor("!geom", (lambda l, n: read_type(Rect, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!geom", rect_regex, Loader=yaml.SafeLoader)

color_regex = re.compile(r'^\$([0-9A-Fa-f][0-9A-Fa-f])+$')
yaml.add_constructor("!color", (lambda l, n: read_type(Color, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver(u'!color', color_regex, Loader=yaml.SafeLoader)



#######################
#    Widget Parsing   #
#######################	

def read_widget(typ, loader, node):
	params = loader.construct_mapping(node, deep=True)
	
	children = params.pop("children", None)

	return Node(typ, initial=children, layout=params)
	
	
recognized_types = (
	'caLabel', 'caLineEdit', 'caTextEntry', 'caMenu', 'caRelatedDisplay',
	'caNumeric', 'caApplyNumeric', 'caSlider', 'caChoice', 'caTextEntry',
	'caMessageButton', 'caToggleButton', 'caSpinbox', 'caByteController',
	'caLabelVertical', 'caGraphics', 'caPolyLine', 'caImage', 'caInclude',
	'caDoubleTabWidget', 'caClock', 'caLed', 'caLinearGauge', 'caMeter',
	'caCircularGauge', 'caMultiLineString', 'caThermo', 'caCartesianPlot',
	'caStripPlot', 'caByte', 'caTable', 'caWaveTable', 'caBitnames',
	'caCamera', 'caCalc', 'caWaterfallPlot', 'caScan2D', 'caLineDraw',
	'caShellCommand', 'caScriptButton', 'caMimeDisplay', 'caFrame',
	'Form'
)

for widget_type in recognized_type:
	yaml.add_constructor("!" + widget_type, (lambda l, n, t=widget_type: read_widget(t, l, n)), Loader=yaml.SafeLoader)
	
yaml.add_constructor("!group", (lambda l, n: read_widget("caFrame", l, n)), Loader=yaml.SafeLoader)
	
	
#####################
#   Include Files   #
#####################

include_regex = re.compile(r'^#include\s*(.*)$')
included_files = []

def read_file(filename):
	the_data_out = ""
	
	with open (filename) as the_file:
		the_data_in = the_file.readlines()
		
		for line in the_data_in:
			check = include_regex.match(line)
			
			if check:
				include_file = check.group(1).strip()
				
				if include_file not in included_files:
					included_files.append(include_file)
					the_data_out += read_file(include_file)
			else:
				the_data_out += line

	return the_data_out
	
	
	
def parse(filename):
	included_files = []
	
	return yaml.safe_load(read_file(filename))
	
