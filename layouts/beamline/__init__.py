from .. import registry

registry.add("Beamline Overview", path=__path__,
	qt_stylesheet = "layout.yml",
	css_stylesheet = "layout.yml",
	required_inputs=[
("SECTOR", "Sector Number"),
("TYPE",   "ID or BM"),
("HUTCHES", 
"""List of data dictionaries describing hutches:
	
    ID: Hutch Lettering
    PREFIX: IOC PV prefix
    SHUTTER: Shutter Permit Call Code
""")], 
example=
"""SECTOR: 1
TYPE: 'BM'

HUTCHES:
    - ID: A
      PREFIX: 1bma
      SHUTTER: FES

    - ID: B
      PREFIX: 1bmb
      SHUTTER: SBS

    - ID: C
      PREFIX: 1bmc
      SHUTTER: SCS
""")
