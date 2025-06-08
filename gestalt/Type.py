import copy
import yaml
from gestalt.Datasheet import *

class PartialSubFormatter:
	def __init__(self, macro):
		self.macro = macro
		
	def __format__(self, format_spec):
		if format_spec:
			return "{" + self.macro + ":" + format_spec + "}"
		else:
			return "{" + self.macro + "}"

class PartialSubDict(dict):
	def __missing__(self, key):
		return PartialSubFormatter(key)



class DataType(object):	
	def __init__(self, typ, val):
		self.typ = typ
		self.macros = []
		self.updates = {}
		
		self.standard = True
		self.dict = False
		self.list = False
		
		if isinstance(val, dict):
			self.standard = False
			self.value = val
			self.dict = True
			
		elif isinstance(val, list) or isinstance(val, tuple):
			self.standard = False
			self.value = list(val)
			self.list = True
			
		elif isinstance(val, str):
			self.value = val
			
		elif isinstance(val, DataType):
			self.value    = val.value
			self.macros   = val.macros
			self.updates  = val.updates
			self.standard = val.standard
			self.dict     = val.dict
			self.list     = val.list
			
		else:
			self.value = str(val)

	def copy(self):
		output  = type(self)(copy.copy(self.value))
		
		for item in self.macros:
			output.macros.append(copy.copy(item))
			
		output.updates = copy.copy(self.updates)
		
		return output
		
	def val(self):	
		if self.standard:
			output = self.value
			
			for macrolist in reversed(self.macros):
				for macro, macro_val in reversed(macrolist.items()):
					try:
						output = output.format_map(PartialSubDict({macro : macro_val }))
					except:
						pass
			
					if self.typ == "list" or self.typ == "dict":
						try:
							check = yaml.safe_load(output)
							
							if self.typ == "list" and isinstance(check, list):
								out = List(check)
								out.macros = self.macros
								return out.val()
								
							if self.typ == "dict" and isinstance(check, dict):
								out = Dict(check)
								out.macros = self.macros
								return out.val()
								
						except:
							pass
						
			return output
					
		elif self.dict:
			output = copy.deepcopy(self.value)
			
			for key, val in output.items():
				if key in self.updates:
					output[key] = self.updates[key]
					continue
				
				for macrolist in reversed(self.macros):
					temp_val = DataType("temp", val)
					temp_val.macros = self.macros
					
					try:
						output[key] = temp_val.val()
						#output[key] = str(val).format_map(PartialSubDict({macro : macro_val}))
					except:
						pass
		
			return output
			
		elif self.list:		
			output = copy.deepcopy(self.value)
			
			for index in range(len(output)):
				if index in self.updates:
					output[index] = self.updates[index]
					continue
				
				index_val = DataType("temp", output[index])
				index_val.macros = self.macros
					
				try:
					output[index] = index_val.val()
				except Exception as e:
					print(e)
					pass
					
			return output
		
		return None
			
		
		
	def apply(self, macros):
		self.macros.append(macros.copy())
		
	def flatten(self):
		return type(self)(self.val())


	def __setitem__(self, key, data):
		self.updates[key] = data
		
	def __getitem__(self, key):
		return self.val()[key]		
		
		
	def __bool__(self):
		if self.val():
			try:
				return bool(int(self.value.lower()))
			except:
				return not ( self.value.lower() == "false" )
				
		return False
		
	def __int__(self):
		return int(self.val())
		
	def __str__(self):
		return str(self.val())
		
	def __repr__(self):
		return self.__str__()
		
	def __float__(self):
		return float(self.val())
		
	def __format__(self, format_spec):
		return str(self).__format__(format_spec)
		

###########################
#     BASIC DATA TYPES    #
###########################

class String(DataType):	
	def __init__(self, data):
		super().__init__("string", data)
		
class Number(DataType):
	def __init__(self, data):
		super().__init__("number", data)
		
	def val(self):
		return int(super().val())
		
	def __format__(self, format_spec):
		return self.val().__format__(format_spec)
				
		
class Double(DataType):
	def __init__(self, data):
		super().__init__("double", data)

	def val(self):
		return float(super().val())
		
			
class Enum(DataType):	
	def __init__(self, data):
		super().__init__("enum", data)

class Set(DataType):
	def __init__(self, data):
		super().__init__("set", data)
		
class Bool(DataType):
	def __init__(self, data):
		super().__init__("bool", data)
		

class Not(String):
	def __init__(self, data):
		super().__init__(data)


###########################
#    GEOMETRY DATA TYPE   #
###########################


class Rect(DataType):
	def __init__(self, data):		
		if isinstance(data, Number):
			super().__init__("rect", "0x{:x}".format(int(data.value)))
			self.macros = data.macros
			self.updates = data.updates
			
		elif isinstance(data, int):
			super().__init__("rect", "0x{:x}".format(data))
			
		else:
			super().__init__("rect", data)
		
			
	def val(self):
		try:
			data = super().val()
			
			self.labels = ["x", "y", "width", "height"]
			
			if self.standard:			
				data = [ int(item) for item in data.split("x")]
			elif self.dict:
				data = [ data.get(key, 0) for key in self.labels ]
					
			temp = []
				
			for i in range(4 - len(data)):
				temp.append(0)
					
			for item in data:
				temp.append(item)
				
			output = dict(zip(self.labels, temp))
			output.update(self.updates)
			
			return output
		except:
			raise Exception("Error resolving Rect datatype from value: " + self.value)
		
	def __getitem__(self, key):
		return int(self.val()[key])
		
	def __str__(self):
		data = self.val()
		return "{x}x{y}x{width}x{height}".format(**data)
		
	def __repr__(self):
		data = self.val()
		return "{x}x{y}x{width}x{height}".format(**data)
						
		
#######################
#   COLOR DATA TYPE   #
#######################

class Color(DataType):
	def __init__(self, data):
		self.labels = ["red", "green", "blue", "alpha"]
		
		super().__init__("color", data)
		
		
	def val(self):
		try:
			data = super().val()
			
			if self.standard:
				data = data.lstrip("$")
				
				# Interpret each 2-char chunk as a hex number
				data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
					
			elif self.dict:
				data = [ data.get(key, None) for key in self.labels ]
				
			temp = [None, None, None, 255]
				
			for i in range(len(data)):
				temp[i] = int(data[i])
					
			output = dict( zip(self.labels, temp))
			output.update(self.updates)
			
			return output
			
		except:
			raise Exception("Error resolving Color datatype from value: " + self.value)
		
	def __str__(self):
		input = self.val()
		output = "${red:02X}{green:02X}{blue:02X}{alpha:02X}"
		
		try:
			return output.format(**input)
		except:
			return ""
	
		
######################
#   FONT DATA TYPE   #
######################

class Font(DataType):
	def __init__(self, data):
		super().__init__("font", data)
		
	def val(self):
		try:			
			data = super().val()
			
			self.labels = ["family", "style", "size"]
			
			if self.standard:
				data = [ item.strip() for item in data.lstrip("-").split("-") ]
			elif self.dict:
				data = [ data.get(key, None) for key in self.labels ]
						
			temp = [None, None, None]
				
			for i in range(len(data)):
				temp[i] = data[i]
				
			output = dict(zip(self.labels, temp))
			output.update(self.updates)
			
			return output
		except:
			raise Exception("Error resolving Font datatype from value: " + self.value)
		
		
		
###########################
#   ALIGNMENT DATA TYPE   #
###########################

class Alignment(DataType):	
	def __init__(self, data):
		super().__init__("align", data)
	
	def val(self):
		try:
			self.labels = [ "vertical", "horizontal" ]
			
			data = super().val()
			
			if self.standard:
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
		except:
			raise Exception("Error resolving Alignment datatype from value: " + self.value)

	def __str__(self):
		output = self.val()
		
		return str(output["vertical"]) + str(output["horizontal"])
			
		
######################
#   LIST DATA TYPE   #
######################

class List(DataType):
	def __init__(self, data):
		super().__init__("list", data)

	def val(self):
		try:
			output = []
			data = super().val()
			
			if self.standard and hasattr(data, 'read'):
				data = yaml.safe_load(data)
				
			if isinstance(data, list):
				return data
				
			return None
		except Exception as e:
			raise Exception("Error resolving List datatype from value: " + self.value)

	def __iter__(self):
		return self.val().__iter__()
	   
	def __str__(self):
		return yaml.dump(self.val())

class Dict(DataType):
	def __init__(self, data):
		super().__init__("dict", data)

	def val(self):
		try:
			output = []
			data = super().val()
			
			if self.standard and hasattr(data, 'read'):
				data = yaml.safe_load(data)
				
			if isinstance(data, dict):
				return data
				
			return None
		except Exception as e:
			raise Exception("Error resolving Dict datatype from value: " + self.value)


	def __iter__(self):		
		return self.val()
		
	def __str__(self):
		return yaml.dump(self.val())

		
