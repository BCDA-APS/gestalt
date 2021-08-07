import re
import yaml

from gestalt.Type import *
from gestalt.Gestalt import Widget, Group

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


set_regex = re.compile(r'^[a-zA-Z0-9_:]+(\s*\|\s*[a-zA-Z0-9_:]+)+$')
yaml.add_constructor("!set",    (lambda l, n: read_type(Set, l, n)),    Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!set", set_regex, Loader=yaml.SafeLoader)
			
enum_regex = re.compile(r'^\w+::\w+$')
yaml.add_constructor("!enum", (lambda l, n: read_type(Enum, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!enum", enum_regex, Loader=yaml.SafeLoader)
			
rect_regex = re.compile(r'^\d+\s*(x\d+\s*)+$')
yaml.add_constructor("!geom", (lambda l, n: read_type(Rect, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!geom", rect_regex, Loader=yaml.SafeLoader)

color_regex = re.compile(r'^\$([0-9A-Fa-f][0-9A-Fa-f])+$')
yaml.add_constructor("!color", (lambda l, n: read_type(Color, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver(u'!color', color_regex, Loader=yaml.SafeLoader)



#######################
#    Widget Parsing   #
#######################


def create_group(loader, node):
	try:
		children = loader.construct_sequence(node)
		return Group(children)
	except:
		children = loader.construct_mapping(node)
		return Group(children)
	
	
	

def read_widget(typ, loader, node):
	params = loader.construct_mapping(node)
	
	return Widget(typ, layout=params)
	
	
recognized_widgets = (
	'caLabel', 'caLineEdit', 'caTextEntry', 'caMenu', 'caRelatedDisplay',
	'caNumeric', 'caApplyNumeric', 'caSlider', 'caChoice', 'caTextEntry',
	'caMessageButton', 'caToggleButton', 'caSpinbox', 'caByteController',
	'caLabelVertical', 'caGraphics', 'caPolyLine', 'caImage', 'caInclude',
	'caDoubleTabWidget', 'caClock', 'caLed', 'caLinearGauge', 'caMeter',
	'caCircularGauge', 'caMultiLineString', 'caThermo', 'caCartesianPlot',
	'caStripPlot', 'caByte', 'caTable', 'caWaveTable', 'caBitnames',
	'caCamera', 'caCalc', 'caWaterfallPlot', 'caScan2D', 'caLineDraw',
	'caShellCommand', 'caScriptButton', 'caMimeDisplay'
)

for widget_type in recognized_widgets:
	yaml.add_constructor("!" + widget_type, (lambda l, n, t=widget_type: read_widget(t, l, n)), Loader=yaml.SafeLoader)


yaml.add_constructor("!group", create_group, Loader=yaml.SafeLoader)
	

def parse(filename):		
	with open(filename) as the_file:
		return yaml.safe_load(the_file)
