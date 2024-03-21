import copy
from gestalt.Datasheet import *

class DataType(object):
	def __init__(self, typ, val):
		self.typ = typ
		self.value = val
		self.defaultvalue = ""
		self.macros = []
		self.updates = {}

	def apply(self, macros):		
		self.macros.append(copy.deepcopy(macros))
				
	def val(self):
		output = copy.deepcopy(self.value)
		
		for macrolist in reversed(self.macros):
			if isinstance(output, dict):
				for key, item in output.items():
					if item is None:
						output[key] = self.defaultvalue
					else:
						try:
							output[key] = str(item).format(**macrolist)
						except:
							pass
			elif isinstance(output, str):
				try:
					output = str(output).format(**macrolist)
				except KeyError:
					pass
					
		if isinstance(output, dict):
			output.update(self.updates)
	
		return output
	
	def __setitem__(self, key, data):
		self.updates[key] = data
		
	def __getitem__(self, key):
		return self.val()[key]

	def __bool__(self):
		return bool(self.val())
		
	def __int__(self):
		return int(self.val())
		
	def __str__(self):
		return str(self.val())
		
	def __float__(self):
		return float(self.val())
		

###########################
#     BASIC DATA TYPES    #
###########################

class String(DataType):
	def __init__(self, data):
		if isinstance(data, String):
			super(String, self).__init__("string", data.value)
			self.macros = data.macros
		else:
			super(String, self).__init__("string", str(data))
	
	def __bool__(self):
		output = super(String, self).__bool__()
		
		if output:
			try:
				output = bool(int(self.value.lower()))
			except:
				output = not ( self.value.lower() == "false" )
				
		return output
	
class Number(DataType):
	def __init__(self, data):
		if isinstance(data, String) or isinstance(data, Number):
			super(Number, self).__init__("number", data.value)
			self.macros = data.macros
		else:
			super(Number, self).__init__("number", data)
	
			
class Double(DataType):
	def __init__(self, data):
		if isinstance(data, String) or isinstance(data, Double):
			super(Double, self).__init__("double", data.value)
			self.macros = data.macros
		else:
			super(Double, self).__init__("double", data)

			
class Enum(DataType):	
	def __init__(self, data):
		if isinstance(data, String) or isinstance(data, Enum):
			super(Enum, self).__init__("enum", data.value)
			self.macros = data.macros
		else:
			super(Enum, self).__init__("enum", data)

	def val(self):
		return str(self.value)
			
class Set(DataType):
	def __init__(self, data):
		if isinstance(data, String) or isinstance(data, Set):
			super(Enum, self).__init__("set", data.value)
			self.macros = data.macros
		else:
			super(Set, self).__init__("set", data)
		
	def val(self):
		return str(self.value)
	
		
class Bool(DataType):
	def __init__(self, val):
		if isinstance(data, String) or isinstance(data, Bool):
			super(Bool, self).__init__("bool", data.value)
			self.macros = data.macros
		else:
			super(Bool, self).__init__("bool", data)
		

class Not(DataType):
	def __init__(self, val):
		if isinstance(data, String) or isinstance(data, Not):
			super(Not, self).__init__("inverse", data.value)
			self.macros = data.macros
		else:
			super(Not, self).__init__("inverse", data)
		
	def val(self):
		return str(self.value)
	

###########################
#    GEOMETRY DATA TYPE   #
###########################


class Rect(DataType):			
	def __init__(self, data):
		if isinstance(data, String) or isinstance(data, Rect):
			super(Rect, self).__init__("rect", data.value)
			self.macros = data.macros
			self.updates = data.updates
		
		elif isinstance(data, Number):
			super(Rect, self).__init__("rect", "0x{:x}".format(int(data.value)))
			self.macros = data.macros
			self.updates = data.updates
			
		elif isinstance(data, int):
			super(Rect, self).__init__("rect", "0x{:x}".format(data))
			
		else:
			super(Rect, self).__init__("rect", data)
		
			
	def val(self):
		data = super(Rect, self).val()
		
		self.labels = ["x", "y", "width", "height"]
		
		if isinstance(data, dict):
			data = [ data.get(key, 0) for key in self.labels ]
				
		elif isinstance(data, str):
			data = [ int(item) for item in data.split("x")]
				
		temp = []
			
		for i in range(4 - len(data)):
			temp.append(0)
				
		for item in data:
			temp.append(item)
			
		output = dict(zip(self.labels, temp))
		output.update(self.updates)
		return output
		
	def __getitem__(self, key):
		return int(self.val()[key])
						
		
#######################
#   COLOR DATA TYPE   #
#######################

class Color(DataType):
	def __init__(self, data):
		self.labels = ["red", "green", "blue", "alpha"]
		
		if isinstance(data, String) or isinstance(data, Color):
			super(Color, self).__init__("color", data.value)
			self.macros = data.macros
			self.updates = data.updates
			
		else:
			super(Color, self).__init__("color", data)
		
	def val(self):
		data = super(Color, self).val()
		
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):
			data = data.lstrip("$")
			
			# Interpret each 2-char chunk as a hex number
			data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
			
		temp = [None, None, None, 255]
			
		for i in range(len(data)):
			temp[i] = data[i]
				
		output = dict( zip(self.labels, temp))
		output.update(self.updates)
		return output
		
	def __str__(self):
		input = self.val()
		output = "${red:2X}{green:2X}{blue:2X}{alpha:2X}"
		
		try:
			return output.format(**input)
		except:
			return ""
	
		
######################
#   FONT DATA TYPE   #
######################

class Font(DataType):
	def __init__(self, data):
		if isinstance(data, String) or isinstance(data, Font):
			super(Font, self).__init__("font", data.value)
			self.macros = data.macros
			self.updates = data.updates
			
		else:
			super(Font, self).__init__("font", data)
		
	def val(self):
		data = super(Font, self).val()
		
		self.labels = ["family", "style", "size"]
		
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):
			data = [ item.strip() for item in data.lstrip("-").split("-") ]
			
		temp = [None, None, None]
			
		for i in range(len(data)):
			temp[i] = data[i]
			
		output = dict(zip(self.labels, temp))
		output.update(self.updates)
		return output
		
		
		
		
###########################
#   ALIGNMENT DATA TYPE   #
###########################

class Alignment(DataType):	
	def __init__(self, data):
		if isinstance(data, String) or isinstance(data, Alignment):
			super(Alignment, self).__init__("align", data.value)
			self.macros = data.macros
			self.updates = data.updates
		else:
			super(Alignment, self).__init__("align", data)
	
	def val(self):
		self.labels = [ "vertical", "horizontal" ]
		
		data = super(Alignment, self).val()
		
		if isinstance(data, str):
			temp = { "vertical" : "Center", "horizontal" : "Center" }
				
			data = data.lower()
			
			if "top" in data:
				temp["vertical"] = "Top"
			if "bottom" in data:
				temp["vertical"] = "Bottom"
			if "left" in data:
				temp["horizontal"] = "Left"
			if "right" in data:
				temp["horizontal"] = "Right"
			
			data = temp
				
		if isinstance(data, dict):
			temp = { "vertical" : "Center", "horizontal" : "Center"}
			
			if "vertical" in data:
				temp["vertical"] = str(data["vertical"]).capitalize()
			
			if "horizontal" in data:
				temp["horizontal"] = str(data["horizontal"]).capitalize()
					
				
			temp.update(self.updates)
			return temp		

	def __str__(self):	
		return str(self.val()["vertical"]) + str(self.val()["horizontal"])
			
