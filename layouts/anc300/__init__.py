from .. import registry

registry.add("ANC300", path=__path__,
	qt_stylesheet = "layout.yml",
	css_stylesheet = "layout.yml",
	pydm_stylesheet = "layout.yml",
	required_inputs=[
("AXES", 
"""Number of Axes
""")], 
example=
"""AXES: 3
""")
