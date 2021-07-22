import re
import yaml

from gestalt.Type import *


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
yaml.add_constructor("!set",    (lambda l, n: read_type(Set, l, n)),    Loader=yaml.SafeLoader)
			
enum_regex = re.compile(r'^\w+::\w+$')
yaml.add_constructor("!enum", (lambda l, n: read_type(Enum, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!enum", enum_regex, Loader=yaml.SafeLoader)
			
rect_regex = re.compile(r'^\d+x\d+$')
yaml.add_constructor("!geom", (lambda l, n: read_type(Rect, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver("!geom", rect_regex, Loader=yaml.SafeLoader)

color_regex = re.compile(r'^\$([0-9A-Fa-f][0-9A-Fa-f])+$')
yaml.add_constructor("!color", (lambda l, n: read_type(Color, l, n)), Loader=yaml.SafeLoader)
yaml.add_implicit_resolver(u'!color', color_regex, Loader=yaml.SafeLoader)


			
			

def parse(filename):		
	with open(filename) as the_file:
		return yaml.safe_load(the_file)
