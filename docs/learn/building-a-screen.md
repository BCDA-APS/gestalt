---
layout: default
title: Building a Screen
parent: Learn
nav_order: 1
---

# Building a Screen
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

This tutorial builds a complete device control screen step by step, introducing layout
containers, templates, and data-driven repetition along the way. It assumes you have
already worked through the [Quick Start](./), so you know how to write a basic layout
file and run Gestalt from the command line.


## Step 1: Screen setup

Create a file called `device.yml`. Start with the Form and a title banner using the
built-in `ScreenHeader` template:

```yaml
#include colors.yml
#include widgets.yml

Form: !Form
    title: "$(P) Device Control"
    margins: 10x5x10x10
    background: $757687

Header: !Apply:ScreenHeader { title: "Device Control" }
```

`margins` uses the format `LeftxTopxRightxBottom` and adds padding around the screen
edges. The `ScreenHeader` template creates a horizontally stretched title banner that
fills the screen width.


## Step 2: Add status readbacks

Below the header, add a vertical flow of readback rows. Use `!VFlow` to stack them
and `!HFlow` to arrange each row horizontally:

```yaml
#include colors.yml

Form: !Form
    title: "$(P) Device Control"
    margins: 10x5x10x10
    background: $757687

Header: !HStretch:Text
    geometry: 0x30
    text: "Device Control"
    font: -Cantarell - Bold
    foreground: *white
    background: *header_blue
    alignment: Center

Readbacks: !VFlow
    geometry: 0x40 x 0x0
    padding: 5
    children:
        - !HFlow
            padding: 10
            children:
                - !Text        { geometry: 100x20, text: "Temperature:", alignment: CenterRight }
                - !TextMonitor { geometry: 120x20, pv: "$(P)$(R)Temp:RBV", background: *transparent }
                - !Text        { geometry: 30x20,  text: "C", alignment: CenterLeft }

        - !HFlow
            padding: 10
            children:
                - !Text        { geometry: 100x20, text: "Pressure:", alignment: CenterRight }
                - !TextMonitor { geometry: 120x20, pv: "$(P)$(R)Pres:RBV", background: *transparent }
                - !Text        { geometry: 30x20,  text: "psi", alignment: CenterLeft }
```

`!VFlow` stacks its children vertically with `padding` pixels of spacing between them.
Each `!HFlow` arranges its children in a horizontal row. You only need to specify
`WidthxHeight` for each widget -- the flows handle positioning.

The `geometry: 0x40 x 0x0` on the VFlow sets its Y position to 40 (below the header)
with width and height of 0 (auto-sized from children).


## Step 3: Use PVReadWrite to simplify

The label + readback + units pattern is so common that Gestalt provides the `PVReadWrite`
template for it. Replace the manual HFlow rows:

```yaml
#include colors.yml
#include widgets.yml

Form: !Form
    title: "$(P) Device Control"
    margins: 10x5x10x10
    background: $757687

Header: !Apply:ScreenHeader { title: "Device Control" }

Readbacks: !VFlow
    geometry: 0x40 x 0x0
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "Temperature:"
            label-width: 100
            read-pv: "$(P)$(R)Temp:RBV"
            read-width: 120
            units: "C"
            units-width: 30

        - !Apply:PVReadWrite
            label: "Pressure:"
            label-width: 100
            read-pv: "$(P)$(R)Pres:RBV"
            read-width: 120
            units: "psi"
            units-width: 30
```

Each `!Apply:PVReadWrite` produces the same label + readback + units row as before,
but in a few lines instead of many. And because each element is only shown when its
parameter is set, you can easily add setpoint controls just by providing more PVs.


## Step 4: Add setpoint controls

Add entry fields and menus by providing the corresponding PV parameters:

```yaml
Controls: !VFlow
    geometry: 0x110 x 0x0
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "Setpoint:"
            label-width: 100
            entry-pv:  "$(P)$(R)Setpoint"
            entry-width: 80
            read-pv:   "$(P)$(R)Setpoint:RBV"
            read-width: 80
            units: "C"
            units-width: 30

        - !Apply:PVReadWrite
            label: "Mode:"
            label-width: 100
            menu-pv:  "$(P)$(R)Mode"
            menu-width: 120
            read-pv:  "$(P)$(R)Mode:RBV"
            read-width: 80
```

The first row has an entry field for typing a setpoint value, plus a readback and units.
The second row has a dropdown menu for selecting from an enum PV.

`PVReadWrite` supports many more elements: `button-pv` for message buttons, `choice-pv`
for radio-button selectors, `led-pv` for status indicators, `enable-pv` for on/off
toggles, and tweak controls. See the
[PVReadWrite reference](../reference/templates/read-write) for the full list.


## Step 5: Use data to drive repetition

If your device has multiple channels, you can use a data file to avoid repeating yourself.

Create a data file called `device_data.yml`:

```yaml
CHANNELS:
    - { N: 1, label: "Channel 1" }
    - { N: 2, label: "Channel 2" }
    - { N: 3, label: "Channel 3" }
    - { N: 4, label: "Channel 4" }
```

Then use `!VRepeat` to generate one row per channel:

```yaml
Channels: !VRepeat
    geometry: 0x170 x 0x0
    repeat-over: "CHANNELS"
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "{label}:"
            label-width: 100
            entry-pv:  "$(P)$(R)Ch{N}:Set"
            entry-width: 80
            read-pv:   "$(P)$(R)Ch{N}:RBV"
            read-width: 80
```

Generate with the data file:

```bash
python gestalt.py --to ui --input device_data.yml --output device.ui device.yml
```

The `!VRepeat` node iterates over the `CHANNELS` list. For each item, it creates a
copy of its children with `{N}` and `{label}` substituted from that item's dictionary.
Changing the data file to have 8 channels instead of 4 regenerates the screen with 8
rows -- no layout changes needed.


## Step 6: Put it all together

Here is the complete layout:

```yaml
#include colors.yml
#include widgets.yml

Form: !Form
    title: "$(P) Device Control"
    margins: 10x5x10x10
    background: $757687

Header: !Apply:ScreenHeader { title: "Device Control" }

Status: !VFlow
    geometry: 0x40 x 0x0
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "Temperature:"
            label-width: 100
            read-pv: "$(P)$(R)Temp:RBV"
            read-width: 120
            units: "C"
            units-width: 30

        - !Apply:PVReadWrite
            label: "Pressure:"
            label-width: 100
            read-pv: "$(P)$(R)Pres:RBV"
            read-width: 120
            units: "psi"
            units-width: 30

Controls: !VFlow
    geometry: 0x110 x 0x0
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "Setpoint:"
            label-width: 100
            entry-pv:  "$(P)$(R)Setpoint"
            entry-width: 80
            read-pv:   "$(P)$(R)Setpoint:RBV"
            read-width: 80
            units: "C"
            units-width: 30

        - !Apply:PVReadWrite
            label: "Mode:"
            label-width: 100
            menu-pv:  "$(P)$(R)Mode"
            menu-width: 120
            read-pv:  "$(P)$(R)Mode:RBV"
            read-width: 80

Channels: !VRepeat
    geometry: 0x170 x 0x0
    repeat-over: "CHANNELS"
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "{label}:"
            label-width: 100
            entry-pv:  "$(P)$(R)Ch{N}:Set"
            entry-width: 80
            read-pv:   "$(P)$(R)Ch{N}:RBV"
            read-width: 80
```

Generate for any platform:

```bash
# caQtDM
python gestalt.py --to ui --input device_data.yml --output device.ui device.yml

# CSS-Phoebus
python gestalt.py --to bob --input device_data.yml --output device.bob device.yml

# PyDM
python gestalt.py --to pydm --input device_data.yml --output device_pydm.ui device.yml
```

---

## What you learned

- **Screen setup**: `!Form` with margins and background, `!Apply:ScreenHeader` for a title banner.
- **Layout containers**: `!VFlow` and `!HFlow` for automatic widget arrangement.
- **Templates**: `!Apply:PVReadWrite` to replace repetitive manual widget groups.
- **Setpoint controls**: Adding entry fields and menus by providing PV parameters.
- **Data-driven repetition**: `!VRepeat` with `repeat-over` to generate rows from a data list.
- **Multi-platform output**: Same layout produces caQtDM, Phoebus, and PyDM screens.

---

## Next steps

- [Template Reference](../reference/templates/) -- Full documentation for all built-in templates.
- [Custom Templates](../guides/custom-templates) -- Learn to write your own reusable templates.
