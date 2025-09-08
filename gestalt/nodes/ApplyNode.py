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

from gestalt.Type import *
from gestalt.nodes.GroupNode import GroupNode

class ApplyNode(GroupNode):
	def __init__(self, template="", layout={}, defaults={}, macros={}, subnodes=[], loc=None):
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
		
		output = {}
		output.update(self.defaults)
		output.update(self.data)
		output.update(self.macros)
		
		to_apply = {}
		to_apply.update(self.defaults)
		to_apply.update(self.data)
		to_apply.update(self.macros)
		
		
		for key, val in output.items():
			to_assign = None
			
			if isinstance(val, bool):
				to_assign = Bool(val)
			elif isinstance(val, int):
				to_assign = Number(val)
			elif isinstance(val, float):
				to_assign = Double(val)
			elif isinstance(val, str):
				to_assign = String(val)
			else:
				to_assign = val
			
			if isinstance(to_assign, DataType):
				to_assign.apply(to_apply)
				to_assign = to_assign.flatten()
				#to_assign.apply(self.data)
				
			macros.update({key : to_assign})
					
		return
