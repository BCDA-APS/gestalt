from .. import registry

registry.add("AreaDetector Common Plugins", path=__path__,
	required_inputs=[
("PLUGINS", 
"""List of plugin data dictionaries:
	
  Instance: Plugin instance name
  Displays: UI Displays to link to
  Args: Arguments to pass to the displays
""")], 
example=
"""PLUGINS:
    - Instance: image1
      Displays: NDStdArrays.ui
      Args: "P=$(P),R=image1:"

    - Instance: Pva1
      Displays: NDPva.ui
      Args: "P=$(P),R=Pva1:"
""")
