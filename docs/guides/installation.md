---
layout: default
title: Installation
parent: Guides
nav_order: 1
---

# Installation
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


## Prerequisites

Gestalt requires **Python 3.9** or later.


## Required packages

Gestalt depends on the following Python packages:

| Package    | Purpose |
|------------|---------|
| **lxml**   | XML generation for caQtDM `.ui` files |
| **PyYAML** | YAML parsing for layout and data files |

Install them with pip:

```bash
pip install lxml pyyaml
```


## Optional packages

| Package       | Purpose |
|---------------|---------|
| **phoebusgen** | Required for generating CSS-Phoebus `.bob` files |
| **tkinter**    | Required for the GUI mode (included with most Python installations) |

```bash
pip install phoebusgen
```

`tkinter` is typically bundled with Python. If it is missing on your system, install it
through your system package manager (e.g., `apt install python3-tk` on Debian/Ubuntu,
`dnf install python3-tkinter` on RHEL/Fedora).


## Install Gestalt

Clone the repository:

```bash
git clone https://github.com/BCDA-APS/gestalt.git
cd gestalt
```

Gestalt runs directly from the source directory -- no build step is needed.


## Verify the installation

Check that Gestalt can run:

```bash
python gestalt.py --help
```

You should see the usage message with available options. If you get import errors,
verify that `lxml` and `pyyaml` are installed in the same Python environment.

To verify that caQtDM output works, create a minimal layout file called `test.yml`:

```yaml
#include colors.yml

Form: !Form
    title: "Test"

Label: !Text
    geometry: 100x20
    text: "It works"
```

Then generate output:

```bash
python gestalt.py --to ui --output test.ui test.yml
```

If `test.ui` is created without errors, your installation is working.

To verify CSS-Phoebus output, run the same command with `--to bob`:

```bash
python gestalt.py --to bob --output test.bob test.yml
```

This requires `phoebusgen` to be installed. If you see an import error for `phoebusgen`,
install it with `pip install phoebusgen`.


## Gestalt's directory structure

```
gestalt/
    gestalt.py          # command-line entry point
    gestalt/            # core library (nodes, generators, type system)
    widgets/            # built-in includes (colors.yml, templates, etc.)
    layouts/            # built-in GUI layouts
    docs/               # documentation
    tests/              # test suite
```

The `widgets/` directory is automatically included in the search path for `#include`
statements -- you do not need to specify it with `--include`.


## Next steps

- [Quick Start](../learn/) -- Generate your first screen in five minutes.
- [Using the Command Line](commandline) -- Generate screens from the command line.
- [Using the GUI](gui) -- Launch the interactive GUI mode.
