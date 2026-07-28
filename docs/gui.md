---
layout: default
title: Using the GUI
nav_order: 2
---

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


## Launching the GUI

Running Gestalt without any arguments will launch into the GUI. Here you can interact with
a set of predefined layout files that are located in the /layouts folder. Dropdown menus
allow you to select whether you will be generating a CSS-Phoebus or caQtDM file and which
layout you will be using.

Upon selecting a layout, a brief description of the layout and the input data necessary
will appear on the left hand side and an example piece of input data will be entered into the
right hand pane. You can edit the input data directly or you can load an existing file off
the disk. Currently, the only input datatype supported in the input pane is YAML.

Once you are satisfied, the "Write Output File" button will allow you to select the output
filename and will run Gestalt to generate the file.


## Adding a New Layout

Once you have learned about how to [write a Gestalt Layout file](layouts.md), you may 
want to expose that layout to users of the GUI. Allowing them to use it to generate their 
own files.

The registration system that the GUI uses is built out of the python module system, so
the only thing that's necessary is to drop a folder in the /layouts folder and write
an '__init__.py' file that configures some variables. Taking a look at one of those
init files:

```python
from .. import registry

registry.add("Multimotor Display", path=__path__,
	qt_stylesheet = "layout.yml",
	css_stylesheet = "layout.yml",
	required_inputs=[
("MOTORS", 
"""Number of motors on screen
"""),
("ASPECT",
"""Aspect Ratio for the motor arrangement
"""),
("PADDING",
"""Pixels between each motor
""")], 
example=
"""MOTORS: 8
ASPECT: 2.0
PADDING: 15
""")
```

The first line imports the GUI's registry. Then, it's just a single call of the
`registry.add` function. This function takes in six arguments; the name of the
layout to display to the user and five keyword arguments.

* **path** - This should always be `__path__` and is used to locate the rest of the
files in the folder.  
* **qt_stylesheet** - The filename of the layout file to use to generate caQtDM screens.  
* **css_stylesheet** - The filename of the layout file to use to generate CSS-Phoebus
screens. Much of the time you can use the exact same file for both outputs, but it's possible
that there are incompatibilities between the two systems.
* **required_inputs** - A list of tuples that provides information about the input
values expected to be provided.
* **example** - The example input text that will be copied into the right hand pane of the GUI.

Optionally, you can also include a file named 'thumbnail.png' in the folder. This image will
be displayed in the lower left corner when the layout is selected to demonstrate an example
of what the outputted screen might look like. The aspect ratio of this thumbnail should be 3:2. 
Apply transparencies on the sides if your screen has a more vertical orientation.
