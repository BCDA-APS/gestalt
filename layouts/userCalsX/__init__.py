from .. import registry

registry.add("userCalc breakout", path=__path__,
	qt_stylesheet = "layout.yml",
	css_stylesheet = "layout.yml",
	required_inputs=[
("NUM_CALCS", "How many lines to generate")], 
example=
"""NUM_CALCS: 10
""")
