---
layout: default
title: Learn
nav_order: 2
has_children: true
---

# Quick Start
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

Generate your first EPICS control screen in under five minutes.


## 1. Create a layout file

Create a file called `hello.yml` with the following contents:

```yaml
#include colors.yml

Form: !Form
    title: "Hello Gestalt"

Title: !Text
    geometry: 200x30
    text: "My First Screen"
    font: -Liberation Sans - Bold
    foreground: *white
    background: *header_blue
    alignment: Center

Status: !TextMonitor
    geometry: 0x40 x 200x20
    pv: "$(P)Status"
    foreground: *black
    background: *transparent
```

This layout defines a screen with two widgets: a static text label and a PV readback monitor.

A few things to notice:
- `#include colors.yml` pulls in Gestalt's built-in color definitions (like `*white`,
  `*header_blue`, `*black`, and `*transparent`). These are YAML anchors that resolve to
  hex color values.
- `!Form` sets properties for the screen window itself.
- `!Text` and `!TextMonitor` are Gestalt node tags. Each one produces a widget in the
  output file.
- `geometry` uses the format `WidthxHeight` or `XxYxWidthxHeight`.
- `font` uses a leading dash: `-FontName` or `-FontName - Style - Size`.
- PV names can contain EPICS macros like `$(P)` that get substituted at runtime.


## 2. Generate output

Run Gestalt from the command line to produce a caQtDM `.ui` file:

```bash
python gestalt.py --to ui --output hello.ui hello.yml
```

Or generate a CSS-Phoebus `.bob` file:

```bash
python gestalt.py --to bob --output hello.bob hello.yml
```

Both commands read the same `hello.yml` layout and produce a screen file in the
requested format. Open the output in caQtDM or Phoebus to see your screen.


## 3. Use a built-in template

Gestalt ships with reusable widget templates. Include `widgets.yml` to get access to
all of them:

```yaml
#include colors.yml
#include widgets.yml

Form: !Form
    title: "Hello Gestalt"

Content: !VFlow
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "Setpoint:"
            entry-pv: "$(P)Setpoint"
            read-pv:  "$(P)Setpoint:RBV"
            units: "mm"

        - !Apply:PVReadWrite
            label: "Speed:"
            menu-pv:  "$(P)Speed"
            read-pv:  "$(P)Speed:RBV"
```

`!Apply:PVReadWrite` expands into a complete horizontal row with a label, input field,
readback, and units display. You only provide the PVs and it assembles everything else
with sensible defaults. Each element only appears when its corresponding parameter is set.

---

## Next steps

- [Core Concepts](../concepts/) -- Learn the vocabulary: nodes, data types, includes, templates, and output formats.
- [Building a Screen](building-a-screen) -- A guided tutorial that builds a complete control screen step by step.
- [Installation](../guides/installation) -- Detailed setup instructions and dependencies.
