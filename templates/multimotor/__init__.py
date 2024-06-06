from .. import registry

registry.add("Multimotor Display", path=__path__,
	qt_stylesheet = "layout.yml",
	required_inputs=[
("MOTORS", 
"""Number of motors on screen
"""),
("ASPECT",
"""Aspect Ratio for the motor arrangement
"""),
("PADDING",
"""Pixels between each motor
""")], 
example=
"""MOTORS: 8
ASPECT: 2.0
PADDING: 15
""")
