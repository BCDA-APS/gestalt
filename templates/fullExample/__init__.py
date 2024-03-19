from .. import registry

registry.add("Full Example", path=__path__,
	css_stylesheet = "layout.yml",
	qt_stylesheet = "layout.yml",
	required_inputs=[
("Inputs", "Number of TextEntry fields"),
("LEDs", "Number of LED widgets"),
("Enable_Shapes", "Whether to display shape widgets"),
("Tank_Color", "Fill color of the Scale Widget")], 
example=
"""Inputs: 10
LEDs: 24
Enable_Shapes: True
Tank_Color: $7FFFD4
""")
