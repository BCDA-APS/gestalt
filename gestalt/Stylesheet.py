import os
import re
import copy
import yaml

from yaml.constructor import ConstructorError

import pprint

from gestalt.nodes import *
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
add_constructors("list",   (lambda l, n: read_type(List,   l, n)))
add_constructors("dict",   (lambda l, n: read_type(Dict,   l, n)))
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

	return Node(typ, loc=node.start_mark, layout=params)

def read_special_node(node_type, loader, node, **kwargs):
	params = {}
	
	try:
		params = loader.construct_mapping(node, deep=True)
	except ConstructorError:
		pass

	return node_type(layout=params, loc=node.start_mark, **kwargs)

def read_special_group(node_type, loader, node, **kwargs):
	params = {}
	
	try:
		params = loader.construct_mapping(node, deep=True)
	except ConstructorError:
		params["children"] = loader.construct_sequence(node, deep=True)
		
	return node_type(layout=params, loc=node.start_mark, **kwargs)
	
	
def read_default_node(loader, node):
	return loader.construct_mapping(node, deep=True)
	

def construct_from_suffix(loader, suffix, node):
	if ":" in suffix:
		cls, sub_suffix = suffix.split(":", maxsplit=1)
		return yaml.SafeLoader.yaml_multi_constructors["!" + cls + ":"](loader, sub_suffix, node)
	else:
		return yaml.SafeLoader.yaml_constructors["!" + suffix](loader, node)

def read_embed_multi(loader, suffix, node):
	# Should be nothing, but might be useful in the future
	params = {}
	
	try:
		params = loader.construct_mapping(node, deep=True)
	except:
		loader.construct_scalar(node)
		
	params["embedding"] = String(suffix)
	
	return EmbedNode(layout=params, loc=node.start_mark)
		
		
def read_template_multi(loader, suffix, node):
	params = loader.construct_sequence(node, deep=True)
	defaults = {}
	template_nodes = []
	
	for item in params:
		if isinstance(item, dict):
			defaults.update(item)
			
		elif isinstance(item, Node):
			template_nodes.append(item)
			
	my_templates[suffix] = (template_nodes, defaults)
		
	return None
		
def read_apply_multi(loader, suffix, node):
	macros = {}
	
	try:
		macros = loader.construct_mapping(node, deep=True)
	except:
		pass
	
	if suffix not in my_templates:
		raise ValueError("Could not find template with name: " + suffix)
		
	template_nodes, defaults = my_templates.get(suffix)
	
	return ApplyNode(defaults=defaults, template=suffix, layout={"children" : template_nodes}, macros=macros, loc=node.start_mark)
	
def read_debug_multi(loader, suffix, node):
	ret_node = construct_from_suffix(loader, suffix, node)
	ret_node.debug = True
	
	return ret_node
	
def read_conditional_multi(loader, suffix, node, check_against=True):
	ret_node = read_special_group(ConditionalNode, loader, node)
	
	if check_against == False:
		ret_node.condition = Not(suffix)
	else:
		ret_node.condition = String(suffix)
		
	return ret_node
	
def read_stretch_multi(loader, suffix, node, flow="vertical"):
	ret_node = construct_from_suffix(loader, suffix, node)
	
	return StretchNode(flow=flow, subnode=ret_node, loc=node.start_mark)
	
def read_stretch_node(loader, node, flow="vertical"):
	try:
		params = loader.construct_mapping(node, deep=True)
		return StretchNode(flow=flow, subnode=next(iter(params.values())), loc=node.start_mark)
	except:
		params = loader.construct_sequence(node, deep=True)
		return StretchNode(flow=flow, subnode=next(iter(params)), loc=node.start_mark)

		
def read_center_multi(loader, suffix, node, flow="vertical"):
	ret_node = construct_from_suffix(loader, suffix, node)
	
	return CenterNode(flow=flow, subnode=ret_node, loc=node.start_mark)
		
def read_center_node(loader, node, flow="vertical"):
	try:
		params = loader.construct_mapping(node, deep=True)
		return CenterNode(flow=flow, subnode=next(iter(params.values())), loc=node.start_mark)
	except:
		params = loader.construct_sequence(node, deep=True)
		return CenterNode(flow=flow, subnode=next(iter(params)), loc=node.start_mark)
		
def read_anchor_multi(loader, suffix, node, flow="vertical"):
	ret_node = construct_from_suffix(loader, suffix, node)
	
	return AnchorNode(flow=flow, subnode=ret_node, loc=node.start_mark)
		
def read_anchor_node(loader, node, flow="vertical"):
	try:
		params = loader.construct_mapping(node, deep=True)
		return AnchorNode(flow=flow, subnode=next(iter(params.values())), loc=node.start_mark)
	except:
		params = loader.construct_sequence(node, deep=True)
		return AnchorNode(flow=flow, subnode=next(iter(params)), loc=node.start_mark)

def read_tab_node(loader, node):
	try:
		params = loader.construct_sequence(node, deep=True)
		return GroupNode("TabNode", layout={"children" : params}, loc=node.start_mark)
	except:
		params = loader.construct_mapping(node, deep=True)
		return GroupNode("TabNode", layout=params, loc=node.start_mark)
		

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
	"StripChart", "Symbol", "Tabs", "Table", "Tank", "TextSymbol", 
	"TextUpdate", "Thermometer", "ThreeDViewer", "WebBrowser", "XYPlot"
)

for widget_type in recognized_types:
	yaml.add_constructor("!" + widget_type, (lambda l, n, t=widget_type: read_node(t, l, n)), Loader=yaml.SafeLoader)
	
add_constructors("Group", (lambda l, n: read_special_group(GroupNode, l, n)))
add_constructors("Anon", (lambda l, n: read_special_group(GroupNode, l, n, anonymous=True)))
add_constructors("Anonymous", (lambda l, n: read_special_group(GroupNode, l, n, anonymous=True)))
	
add_constructors("Grid", (lambda l, n: read_special_node(GridNode, l, n)))

add_constructors("Conditional", (lambda l, n: read_special_node(ConditionalNode, l, n)))
add_multi_constructors("If:",    (lambda l, s, n: read_conditional_multi(l, s, n, check_against=True)))
add_multi_constructors("IfNot:", (lambda l, s, n: read_conditional_multi(l, s, n, check_against=False)))

add_multi_constructors("Template:", read_template_multi)
add_multi_constructors("Apply:",   read_apply_multi)

add_multi_constructors("Debug:",   read_debug_multi)
add_constructors("Defaults", read_default_node)

add_multi_constructors("Embed:", read_embed_multi)

add_constructors("spacer", (lambda l, n: read_special_node(SpacerNode, l, n)))
	
add_constructors("Flow",  (lambda l, n: read_special_group(FlowNode, l, n, flow="vertical")))
add_constructors("VFlow", (lambda l, n: read_special_group(FlowNode, l, n, flow="vertical")))
add_constructors("HFlow", (lambda l, n: read_special_group(FlowNode, l, n, flow="horizontal")))
	
add_constructors("Repeat",  (lambda l, n: read_special_node(RepeatNode, l, n,  flow="vertical")))
add_constructors("VRepeat", (lambda l, n: read_special_node(RepeatNode, l, n,  flow="vertical")))
add_constructors("HRepeat", (lambda l, n: read_special_node(RepeatNode, l, n,  flow="horizontal")))

add_multi_constructors("Stretch:",  (lambda l, s, n: read_stretch_multi(l, s, n, flow="vertical")))
add_multi_constructors("VStretch:", (lambda l, s, n: read_stretch_multi(l, s, n, flow="vertical")))
add_multi_constructors("HStretch:", (lambda l, s, n: read_stretch_multi(l, s, n, flow="horizontal")))
add_multi_constructors("AStretch:", (lambda l, s, n: read_stretch_multi(l, s, n, flow="all")))

add_constructors("Stretch",  (lambda l, n: read_stretch_node(l, n, flow="vertical")))
add_constructors("VStretch", (lambda l, n: read_stretch_node(l, n, flow="vertical")))
add_constructors("HStretch", (lambda l, n: read_stretch_node(l, n, flow="horizontal")))
add_constructors("AStretch", (lambda l, n: read_stretch_node(l, n, flow="all")))

add_multi_constructors("Center:",  (lambda l, s, n: read_center_multi(l, s, n, flow="vertical")))
add_multi_constructors("VCenter:", (lambda l, s, n: read_center_multi(l, s, n, flow="vertical")))
add_multi_constructors("HCenter:", (lambda l, s, n: read_center_multi(l, s, n, flow="horizontal")))
add_multi_constructors("ACenter:", (lambda l, s, n: read_center_multi(l, s, n, flow="all")))

add_constructors("Center",  (lambda l, n: read_center_node(l, n, flow="vertical")))
add_constructors("VCenter", (lambda l, n: read_center_node(l, n, flow="vertical")))
add_constructors("HCenter", (lambda l, n: read_center_node(l, n, flow="horizontal")))
add_constructors("ACenter", (lambda l, n: read_center_node(l, n, flow="all")))

add_multi_constructors("Anchor:",  (lambda l, s, n: read_anchor_multi(l, s, n, flow="vertical")))
add_multi_constructors("VAnchor:", (lambda l, s, n: read_anchor_multi(l, s, n, flow="vertical")))
add_multi_constructors("HAnchor:", (lambda l, s, n: read_anchor_multi(l, s, n, flow="horizontal")))
add_multi_constructors("AAnchor:", (lambda l, s, n: read_anchor_multi(l, s, n, flow="all")))

add_constructors("Anchor",  (lambda l, n: read_anchor_node(l, n, flow="vertical")))
add_constructors("VAnchor", (lambda l, n: read_anchor_node(l, n, flow="vertical")))
add_constructors("HAnchor", (lambda l, n: read_anchor_node(l, n, flow="horizontal")))
add_constructors("AAnchor", (lambda l, n: read_anchor_node(l, n, flow="all")))

add_constructors("TabbedGroup",    (lambda l, n: read_special_node(TabbedGroupNode, l, n)))
add_constructors("TabbedRepeat",   (lambda l, n: read_special_node(TabbedRepeatNode, l, n)))
add_constructors("Tab",            (lambda l, n: read_tab_node(l, n)))

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
add_constructors("Calc",           (lambda l, n: read_special_node(CalcNode, l, n)))
add_constructors("Include",        (lambda l, n: read_special_node(IncludeNode, l, n)))


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
			check_locations = copy.copy(includes_locations)
			
			current_dir = os.path.dirname(filename)
			
			if current_dir not in check_locations:
				check_locations.append(current_dir)
			
			if check:
				include_file = check.group(1).strip()
				include_file_fullpath = ""
				
				for check_dir in check_locations:
					path = os.path.abspath(check_dir + "/" + include_file)
						
					if os.path.exists(path):
						include_file_fullpath = path
						break
					
				if include_file_fullpath == "":
					print( "Include file does not exist in path (" + include_file + ")")
					continue
				
				
				if include_file_fullpath not in included_files:
					included_files.append(include_file_fullpath)
					the_data_out += read_file(include_file_fullpath, includes_locations, included_files)
					
			else:
				the_data_out += line
				
	return the_data_out
	
	
	
def render_sort(item):
	check = item[1]
	if not isinstance(check, Node):
		return 0
	else:
		return int(check["render-order"])
	
def parse(filename, includes_dirs):
	return dict(sorted(yaml.safe_load(read_file(filename, includes_dirs, [])).items(), key=render_sort))
