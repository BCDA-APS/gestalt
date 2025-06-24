"""
Conditionally adds children widgets into the final output based upon a specified macro in the
input data.

The macro named by the `condition` macro is parsed and treated as a truthy value in python. If
the macro's data is equivalent to a true value, then the conditional's contents are included in
the resulting UI screen. Otherwise, none of the children widgets are included. The condition can
be negated by using the '!Not' type indicator.

Two aliases are also allowed, '!If' and '!IfNot'. These include the necessary condition in their tag
name. So, using the tag '!If:my-condition' would be equivalent to creating a '!Conditional' with the
condition of '"my-condition"'. And '!IfNot:my-condition' is the equivalent of creating a '!Conditional'
with the condition of '!Not "my-condition"'.

* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to conditionally include |
| condition    | String | The name of a macro that will determine the children widget's inclusion |
| background   | Color  | A fill color behind the entirety of all children |
| border-color | Color  | The color of the group's border surrounding the children widgets |
| border-width | Number | The thickness of the group's border in pixels |
| visibility   | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
HaveLED: !conditional
    condition: "INCLUDE_LED"
    
    geometry: 0x20 x 0x0
    
    children:
        - !LED
            pv: "xxx:yyy:bi.VAL"
            true-color: *alarm_red
            false-color: *alarm_green
            
            border-color: *transparent
            
            geometry: 15x0 x 22x22
            
SimplerVersion: !If:INCLUDE_LED
    - !LED
        pv: "xxx:yyy:bi.VAL"
        true-color: *alarm_red
        false-color: *alarm_green
        
        border-color: *transparent
        
        geometry: 15x0 x 22x22

```
"""

from gestalt.Type import *

from gestalt.nodes.GroupNode import GroupNode

class ConditionalNode(GroupNode):
	def __init__(self, layout={}, loc=None):
		super(ConditionalNode, self).__init__("caFrame", layout=layout, loc=loc)
		
		self.condition = self.pop("condition", "")
		
		for item in self:
			self["render-order"] = max(int(item["render-order"]), int(self["render-order"]))
			self["z-order"]      = max(int(item["z-order"]), int(self["z-order"]))
		
		self.tocopy.append("condition")
		
	
	def apply(self, generator):
		data = yield
		
		invert = isinstance(self.condition, Not)
		
		my_condition = String(self.condition)
		my_condition.apply(data)
		
		conditional = None
		
		try:
			conditional = data[str(my_condition)]
		except KeyError:
			if "{" in my_condition.value:
				conditional = str(my_condition)

		if bool(conditional) != invert:
			for child in self.children:				
				applier = child.apply(generator)
				
				for increment in applier:
					child_macros = copy.copy(data)
					
					try:
						widget = applier.send(child_macros)
						yield widget
					except:
						break
				
					data = yield
