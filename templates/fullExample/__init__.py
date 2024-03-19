from .. import registry

registry.add("Full Example", path=__path__,
	css_stylesheet = "layout.yml",
	qt_stylesheet = "layout.yml",
	required_inputs=[
("INDICES", 
"""List of numbers indicating each userCalc to link:
	
  N: index of userCalc
""")], 
example=
"""INDICES:
    - N: 0
    - N: 1
    - N: 2
    - N: 3
    - N: 4
    - N: 5
    - N: 6
    - N: 7
    - N: 8
    - N: 9
""")
