"""
Apply and Template are special tags that are used to save and restore sets of nodes and provide
them with user-defined macros to fill out their attributes. Both apply and template are tags applied
to a name that gets associated with the set of nodes. 

So, when defining a template that you wish to refer to as "io_label", you would use the type 
"!Template:io_label". Then, when including those templated nodes into a different part of your
yaml file, you would use "!Apply:io_label".

A Template definition is a list with a single Node and an optional set of defaults for the macros used
within the Template. Defaults are just a dictionary of names and values, but can be tagged with the do-nothing 
tag "!Defaults" to make the intention clear. 

For the Apply node, its definition is a dictionary with a set of macros you wish to provide the Template.

* **Example**

```yaml

LblRbkTemplate: !Template:lbl_rbk
    - !Defaults
        spacing: 10
        
    - !hflow
        padding: "{spacing}"
        
        children:
            - !Text { geometry: 150x20, text: "{TITLE}" }
            - !TextMonitor
                <<: *FixedFeedback
                pv: "$(P){PV}"


Status: !hcenter:hflow
    geometry: 20x65 x 0x0
    padding: 20

    children:
        - !vflow
            padding: 5
        
            children:
                - !Apply:lbl_rbk { TITLE: "Model Name",  PV: "ModelName" }
                - !Apply:lbl_rbk { TITLE: "Serial Num",  PV: "SerialNumber" }                            
                - !Apply:lbl_rbk { TITLE: "LJM Version", PV: "LJMVersion" }
                    
        - !vflow
            padding: 5
        
            children:
                - !Apply:lbl_rbk { TITLE: "Firmware Version", PV: "FirmwareVersion" }                    
                - !Apply:lbl_rbk { TITLE: "Temperature (C)",  PV: "DeviceTemperature" }
                - !Apply:lbl_rbk { TITLE: "Driver Version",   PV: "DriverVersion" }

```
"""

import copy

from gestalt.Type import *
from gestalt.nodes.GroupNode import GroupNode

def _wrap_datatype(val):
	if isinstance(val, bool):
		return Bool(val)
	elif isinstance(val, int):
		return Number(val)
	elif isinstance(val, float):
		return Double(val)
	elif isinstance(val, str):
		return String(val)
	return val

class ApplyNode(GroupNode):
	def __init__(self, template="", layout=None, defaults=None, macros=None, subnodes=None, loc=None):
		if layout is None:
			layout = {}
		if defaults is None:
			defaults = {}
		if macros is None:
			macros = {}
		if subnodes is None:
			subnodes = []
		super(ApplyNode, self).__init__("Apply", layout=layout, loc=loc, anonymous=True)
				
		self.defaults = defaults
		self.macros = macros
		
		self.template = template
		
		for item in self:
			self["render-order"] = max(int(item["render-order"]), int(self["render-order"]))
			self["z-order"]      = max(int(item["z-order"]), int(self["z-order"]))
		
		self.tocopy.append("macros")
		self.tocopy.append("defaults")
		self.tocopy.append("template")
		
	def initApply(self, data):
		super().initApply(data)
		self.data = data
		
	def updateMacros(self, output, macros):		
		super().updateMacros(output, macros)

		explicit_macros = copy.deepcopy(self.macros)
		bound_macros = {}

		for key, val in explicit_macros.items():
			to_assign = _wrap_datatype(val)

			if isinstance(to_assign, DataType):
				to_assign.apply(self.data)
				to_assign = to_assign.flatten()

			bound_macros[key] = to_assign

		merged = {}
		merged.update(self.defaults)
		merged.update(self.data)
		merged.update(bound_macros)

		for key, val in merged.items():
			if key in bound_macros:
				macros[key] = bound_macros[key]
				continue

			to_assign = _wrap_datatype(val)

			if isinstance(to_assign, DataType):
				to_assign.apply(merged)
				to_assign = to_assign.flatten()

			macros[key] = to_assign

		return
