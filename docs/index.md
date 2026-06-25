---
layout: default
title: Home
nav_order: 1
---

# GESTALT

**G**enerating **E**PICS **S**creens **T**hrough **A**ssembling **L**ayout **T**emplates
{: .fs-5 }

Gestalt is a Python tool that generates EPICS control system GUI screens from YAML layout
files. Write your screen once, then generate output for caQtDM, CSS-Phoebus, or PyDM.

---

## What it looks like

A short YAML layout:

```yaml
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

Run gestalt to produce a `.ui` file for caQtDM, a `.bob` file for Phoebus, or either
format for PyDM -- all from the same layout.

```
python gestalt.py --to ui --output status.ui layout.yml
python gestalt.py --to bob --output status.bob layout.yml
```

---

## Documentation

[Learn](learn/){: .btn .mr-2 }
Quick start tutorial and guided screen-building walkthrough.

[Guides](guides/){: .btn .mr-2 }
Installation, command-line usage, custom templates, and build integration.

[Reference](reference/){: .btn .mr-2 }
Complete reference for all node types and built-in templates.

[Concepts](concepts/){: .btn .mr-2 }
Core concepts, macro resolution, and architecture.
