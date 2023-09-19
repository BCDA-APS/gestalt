from .. import registry

registry.add("Beamline Overview", path=__path__,
	required_inputs=[
("SECTOR", "Sector Number"),
("TYPE",   "ID or BM"),
("HUTCHES", 
"""List of data dictionaries describing hutches:
	
    ID: Hutch Lettering
    PREFIX: IOC PV prefix
""")], 
example=
"""SECTOR: 1
TYPE: 'BM'

HUTCHES:
    - ID: A
      PREFIX: 1bma

    - ID: B
      PREFIX: 1bmb

    - ID: C
      PREFIX: 1bmc
""")
