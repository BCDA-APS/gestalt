"""
A button that will trigger the running of a selected shell command

These shell commands are detailed by the attribute `commands` which is a list of
dictionaries. Within each dictionary, the following values can be defined:

* label   - The display name for the command to run
* command - The command and all arguments that will be executed

<br>


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| commands   | List   | A list of dictionaries describing the commands that can be run |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
ExampleCommand: !ShellCommand
    geometry: 10x10 x 80x20
    
    text: "Say"
    
    commands: 
        - { label: "Hello",   command: "echo 'Hello'"  }
        - { label: "Goodbye", command: "echo 'Goodbye'"}
```
"""

from gestalt.Type import *
from gestalt.nodes.Node import Node

class ShellCommandNode(Node):
	def __init__(self, name=None, layout={}, loc=None):
		self.proto_commands = List(layout.pop("commands", []))
	
		super(ShellCommandNode, self).__init__("ShellCommand", name=name, layout=layout, loc=loc)
		
		self.setDefault(String,    "text",       "")
		self.setDefault(Color,     "foreground", "$000000")
		self.setDefault(Color,     "background", "$57CAE4")
		self.setDefault(Font,      "font",       "-Liberation Sans - Regular - 12")
		self.setDefault(Alignment, "alignment",  "Center")
		
		self.makeInternal(List, "commands", [])
		
		self.tocopy.append("proto_commands")

			
	def initApply(self, macros):
		copy_commands = copy.deepcopy(self.proto_commands)
		copy_commands.apply(macros)
		
		output = []
		
		for item in copy_commands:
			a_command = Dict(item)
			a_command.apply(macros)
			output.append(a_command.val())
			
		self["commands"] = List(output)
