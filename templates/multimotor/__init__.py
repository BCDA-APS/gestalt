from .. import registry

registry.add("Multimotor Display", path=__path__,
	required_inputs=[
("MOTORS", 
"""Motor index list:
	
  M: Motor number 
""")], 
example=
"""MOTORS:
    - M: 1
    - M: 2
    - M: 3
    - M: 4
    - M: 5
    - M: 6
    - M: 7
    - M: 8
""")
