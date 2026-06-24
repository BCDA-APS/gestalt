---
layout: default
title: Concepts
nav_order: 5
has_children: true
---

# Core Concepts
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

This page introduces the key ideas behind Gestalt. Understanding these concepts will help
you read and write layout files effectively.


## Layout files

A layout file is a YAML document that describes the structure of a control screen. Gestalt
reads this file, builds an internal tree of nodes, and then writes out a UI file in the
requested format.

```yaml
#include colors.yml

Form: !Form
    title: "My Screen"

Label: !Text
    geometry: 100x20
    text: "Hello"
```

Every layout file has:
- One or more `#include` statements to pull in shared definitions (colors, templates).
- A `!Form` entry that sets screen-level properties (title, size, background color, margins).
- One or more named widget entries.

The top-level keys (`Form`, `Label`) are just names -- they identify each entry in the
file. The YAML tags (`!Form`, `!Text`) tell Gestalt what kind of node to create.


## Nodes

Nodes are the building blocks of a layout. There are four categories:

### Widgets

Widgets produce visible elements in the output screen. Each widget type maps to a
platform-specific control:

| Gestalt Widget   | caQtDM           | CSS-Phoebus      | PyDM              |
|------------------|------------------|-------------------|--------------------|
| `!Text`          | caLabel          | Label             | PyDMLabel          |
| `!TextMonitor`   | caLineEdit       | TextUpdate        | PyDMLineEdit       |
| `!TextEntry`     | caTextEntry      | TextEntry         | PyDMLineEdit       |
| `!LED`           | caLed            | LED               | PyDMBitIndicator   |
| `!Menu`          | caMenu           | ComboBox          | PyDMEnumComboBox   |
| `!MessageButton` | caMessageButton  | ActionButton      | PyDMPushButton     |
| `!Slider`        | caSlider         | Scrollbar         | PyDMSlider         |
| `!Spinner`       | caNumeric        | Spinner           | PyDMSpinbox        |

The full list is in the [Node Reference](../reference/nodes/).

### Layout containers

Layout nodes arrange their children automatically:

- `!HFlow` / `!VFlow` -- Stack children horizontally or vertically with configurable padding.
- `!HRepeat` / `!VRepeat` -- Repeat children once per item in a data list or count.
- `!Grid` -- Arrange repeated children in a grid with a configurable aspect ratio.
- `!Group` -- A container with optional border and background, children positioned manually.
- `!TabbedGroup` -- Children organized into selectable tabs.

### Positioners

Positioners modify where a widget is placed relative to its parent:

- `!HCenter` / `!VCenter` -- Center a widget horizontally or vertically.
- `!HStretch` / `!VStretch` / `!AStretch` -- Stretch a widget to fill its parent's width, height, or both.
- `!HAnchor` / `!VAnchor` -- Anchor a widget to an edge of its parent.

Positioners are used as prefixes on other tags: `!HCenter:Text`, `!VStretch:TextMonitor`.

### Logical nodes

These nodes control structure without producing visible widgets themselves:

- `!Template` / `!Apply` -- Define and instantiate reusable widget groups.
- `!If` / `!IfNot` -- Conditionally include children based on a value.
- `!Embed` -- Provide overridable default content.
- `!Include` -- Pull in content from another file.


## Data types

Gestalt automatically infers data types from values in your layout:

### Colors

Colors use a `$` prefix followed by hex digits: `$RRGGBB` or `$RRGGBBAA`.

```yaml
background: $FF0000      # red
foreground: $00000080     # black at 50% opacity
```

The `colors.yml` include file defines named colors as YAML anchors. Reference them
with `*`:

```yaml
#include colors.yml

foreground: *white
background: *alarm_red
```

### Geometry

Geometry specifies position and size using numbers separated by `x`:

```yaml
geometry: 200x30           # width=200, height=30
geometry: 10x40 x 200x30   # x=10, y=40, width=200, height=30
```

When using layout containers like `!VFlow`, you typically only need `WidthxHeight`.

### Fonts

Fonts use a leading dash. Style and size are optional, separated by additional dashes:

```yaml
font: -Liberation Sans                     # just the family
font: -Liberation Sans - Bold              # family + style
font: -DejaVu Sans Mono - regular - 16     # family + style + size
```

In most cases, widget height controls the rendered font size, so specifying a pixel
size in the font string is unnecessary.

### Alignment

Text alignment combines a vertical and horizontal keyword:

```yaml
alignment: Center          # centered both ways
alignment: CenterRight     # vertically centered, right-aligned
alignment: TopLeft         # top-left corner
alignment: BottomRight     # bottom-right corner
```

Vertical options: `Top`, `Center`/`Middle`, `Bottom`.  
Horizontal options: `Left`, `Center`/`Middle`, `Right`.

### Explicit type tags

In rare cases where automatic inference is ambiguous, you can force a specific type
with an explicit tag: `!bool`, `!number`, `!double`, `!string`, `!color`, `!font`,
`!geom`, `!align`, `!enum`, or `!set`. This is mainly needed when setting Qt-specific
enumeration values that don't use the double-colon format:

```yaml
more_screens: !caRelatedDisplay
    stackingMode: !enum Menu
```

The output-independent widgets (like `!TextMonitor`, `!LED`, etc.) set their parameter
types automatically, so explicit tags are rarely needed.


## Includes

The `#include` directive pulls in definitions from another YAML file. Gestalt searches
for included files in:

1. The directory containing the current layout file.
2. Gestalt's built-in `widgets/` directory.
3. Any directories specified with the `--include` command-line flag.

```yaml
#include colors.yml           # built-in color definitions
#include widgets.yml          # all built-in widget templates
#include on-off.yml           # just the OnOffText/OnOffLED templates
```

The most commonly used includes are:
- `colors.yml` -- Named colors (`*white`, `*black`, `*alarm_red`, `*edit_blue`, etc.).
- `widgets.yml` -- All built-in widget templates.
- `color-schemes.yml` -- Preset attribute bundles for common widget styles.


## Templates and Apply

Templates let you define a reusable group of widgets with configurable parameters.
The `!Template` tag defines one, and `!Apply` instantiates it:

```yaml
_MyIndicator: !Template:MyIndicator
    - !Defaults
        label: "Status"
        size: 20
    - !HFlow
        padding: 5
        children:
            - !Text { geometry: 80x{size}, text: "{label}" }
            - !LED  { geometry: {size}x{size}, pv: "{pv}" }

# Use it:
Ind1: !Apply:MyIndicator { pv: "$(P)Status1", label: "Pump" }
Ind2: !Apply:MyIndicator { pv: "$(P)Status2", label: "Valve" }
```

Key points:
- Template names are prefixed with `_` at the top level -- this tells Gestalt they are
  definitions, not widgets to render.
- `!Defaults` sets default values for template parameters.
- Parameters are referenced with `{name}` syntax in property values.
- `!Apply:TemplateName` creates an instance, overriding any defaults with provided values.

Gestalt ships with several built-in templates (PVReadWrite, OnOffLED, DigitalBitList,
etc.). See the [Template Reference](../reference/templates/) for the full list.


## Data files

Layouts can accept external input data that gets substituted into the template as macros.
Data is provided via the `--input` flag:

```bash
python gestalt.py --to ui --input data.yml --output screen.ui layout.yml
```

A typical data file (`data.yml`):

```yaml
MOTORS: 8
ASPECT: 2.0
PADDING: 15
```

In the layout, these values are referenced with `{NAME}` syntax:

```yaml
Grid: !Grid
    repeat-over: "MOTORS"
    aspect-ratio: "{ASPECT}"
    padding: "{PADDING}"
    children:
        - !Apply:EmbeddedMotor
            motor-pv: "$(P)$(M{N})"
```

Data files can be YAML, JSON, INI, or EPICS substitutions format. Gestalt auto-detects
the format from the file extension, or you can specify it with `--from`.


## Output formats

Gestalt generates screens for three EPICS display managers from the same layout file:

| Format      | Flag         | Extension | Display Manager |
|-------------|-------------|-----------|-----------------|
| caQtDM      | `--to ui`   | `.ui`     | caQtDM          |
| CSS-Phoebus | `--to bob`  | `.bob`    | Phoebus         |
| PyDM        | `--to pydm` | `.ui`     | PyDM            |

The layout file is identical across all three. Gestalt handles the translation to each
platform's native widget types, property names, and file format internally.

---

## Next steps

- [Building a Screen](../learn/building-a-screen) -- Build a complete control screen with a guided tutorial.
- [Macro Resolution](macros) -- How macro substitution works under the hood.
- [Architecture](architecture) -- How Gestalt processes layout files.
- [Node Reference](../reference/nodes/) -- Full documentation for every node type.
- [Template Reference](../reference/templates/) -- Documentation for built-in templates.
