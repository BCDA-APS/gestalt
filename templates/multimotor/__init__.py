from .. import registry

registry.add("Multimotor Display", path=__path__,
	qt_stylesheet = "layout.yml",
	required_inputs=[
("MOTORS", 
"""Number of motors on screen
""")], 
example=
"""MOTORS: 8
""")
