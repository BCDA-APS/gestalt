from .. import registry

registry.add("LabJack DAQ Screen", path=__path__,
	qt_stylesheet = "layout.yml",
	required_inputs=[
("", 
"""
""")], 
example=
"""TITLE: "LabJack T8 Box $(P)"
FIO:
  - { Label: "0", N: 0, Enabled: 1 }
  - { Label: "1", N: 1, Enabled: 1 }
  - { Label: "2", N: 2, Enabled: 1 }
  - { Label: "3", N: 3, Enabled: 1 }
  - { Label: "4", N: 4, Enabled: 1 }
  - { Label: "5", N: 5, Enabled: 1 }
  - { Label: "6", N: 6, Enabled: 1 }
  - { Label: "7", N: 7, Enabled: 1 }

EIO:
  - { Label: "8",  N: 8, Enabled: 1 }
  - { Label: "9",  N: 9, Enabled: 1 }
  - { Label: "10", N: 10, Enabled: 1 }
  - { Label: "11", N: 11, Enabled: 1 }
  - { Label: "12", N: 12, Enabled: 1 }
  - { Label: "13", N: 13, Enabled: 1 }
  - { Label: "14", N: 14, Enabled: 1 }
  - { Label: "15", N: 15, Enabled: 1 }

CIO:
  - { Label: "16",  N: 16, Enabled: 1 }
  - { Label: "17",  N: 17, Enabled: 1 }
  - { Label: "18",  N: 18, Enabled: 1 }
  - { Label: "19",  N: 19, Enabled: 1 }

MIO:
  - { Label: "20",  N: 20, Enabled: 1 }
  - { Label: "21",  N: 21, Enabled: 1 }
  - { Label: "22",  N: 22, Enabled: 1 }

NUM_ANALOG_INPUTS: 14
NUM_ANALOG_OUTPUTS: 6
""")
