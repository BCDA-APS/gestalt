# GESTALT

**G**enerating **E**PICS **S**creens **T**hrough **A**ssembling **L**ayout **T**emplates

Gestalt is a Python tool that generates EPICS control system GUI screens from YAML
layout files. Write your screen layout once, then generate output for caQtDM, CSS-Phoebus,
or PyDM.


## Requirements

* Python >= 3.9
* lxml
* PyYAML

Optional:

* phoebusgen -- required for generating CSS-Phoebus `.bob` files
* PyQt5 -- required for the GUI mode
* tkinter -- used for font measurement (included with most Python installations)


## Quick Start

Install dependencies:

```bash
pip install lxml pyyaml
```

Create a layout file (`hello.yml`):

```yaml
#include colors.yml
#include widgets.yml

Form: !Form
    title: "$(P) Status"

Header: !Apply:ScreenHeader { title: "Device Status" }

Controls: !VFlow
    geometry: 0x35 x 0x0
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "Setpoint:"
            entry-pv: "$(P)$(R)Setpoint"
            read-pv:  "$(P)$(R)Setpoint:RBV"
            units: "mm"

        - !Apply:PVReadWrite
            label: "Speed:"
            menu-pv:  "$(P)$(R)Speed"
            read-pv:  "$(P)$(R)Speed:RBV"
```

Generate a screen:

```bash
# caQtDM
python gestalt.py --to ui --output hello.ui hello.yml

# CSS-Phoebus (requires phoebusgen)
python gestalt.py --to bob --output hello.bob hello.yml

# PyDM
python gestalt.py --to pydm --output hello_pydm.ui hello.yml
```


## Using the GUI

Running gestalt without arguments launches the GUI, which provides a set of predefined
layouts with interactive data editing and file generation:

```bash
python gestalt.py
```

The GUI requires PyQt5 (`pip install pyqt5`).


## Documentation

[Full Documentation](https://bcda-aps.github.io/gestalt/)
