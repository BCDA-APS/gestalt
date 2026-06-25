---
layout: default
title: Custom Templates
parent: Guides
nav_order: 4
---

# Custom Templates
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

Templates are the primary mechanism for creating reusable widget groups in Gestalt. This
page covers how to write your own templates, from simple wrappers to complex configurable
components like the built-in `PVReadWrite`.


## Defining a template

A template is defined with the `!Template:Name` tag. The definition has two parts: a
`!Defaults` block that declares parameters with default values, and one or more nodes
that make up the template body.

```yaml
_StatusIndicator: !Template:StatusIndicator
    - !Defaults
        label: "Status"
        size: 20
        label-width: 80
        true-color: $00FF00
        false-color: $FF0000

    - !HFlow
        padding: 5
        children:
            - !Text
                geometry: "{label-width}x{size}"
                text: "{label}"
                alignment: CenterRight
            - !LED
                geometry: "{size}x{size}"
                pv: "{pv}"
                true-color: "{true-color}"
                false-color: "{false-color}"
```

Key points:

- **Naming convention**: The top-level YAML key uses a `_` prefix (`_StatusIndicator`)
  by convention to visually distinguish template definitions from rendered content.
  The `_` is not functionally required -- template definitions are not rendered because
  `!Template` registers the template and produces no output. The name after `!Template:`
  is the name used with `!Apply`.

- **`!Defaults` block**: Every parameter used in the template body should have a default
  value here, except parameters that are required (like `pv` above, which has no default
  and must be provided at every call site).

- **Parameter references**: Use `{name}` syntax in property values. Parameters are
  resolved at apply time, substituting provided values over defaults.


## Using a template

Instantiate a template with `!Apply:Name`, providing values for any parameters you
want to override:

```yaml
Pump: !Apply:StatusIndicator
    pv: "$(P)Pump:Status"
    label: "Pump"

Valve: !Apply:StatusIndicator
    pv: "$(P)Valve:Status"
    label: "Valve"
    true-color: $0000FF
```

Any parameter not provided falls back to the default defined in the template.


## Default chaining

Default values can reference other defaults. This lets you define a single "master"
parameter that cascades to multiple properties:

```yaml
_ConfigRow: !Template:ConfigRow
    - !Defaults
        height: 20
        element-width: 80

        label-width: "{element-width}"
        entry-width: "{element-width}"
        read-width:  "{element-width}"

        label-height: "{height}"
        entry-height: "{height}"
        read-height:  "{height}"
    # ...
```

Setting `element-width: 120` at apply time will cascade to `label-width`, `entry-width`,
and `read-width` unless they are individually overridden.


## Templates with layout containers

Templates commonly wrap their content in a layout container for automatic arrangement:

```yaml
_LabeledEntry: !Template:LabeledEntry
    - !Defaults
        label: ""
        height: 20
        label-width: 100
        entry-width: 80
        spacing: 10

    - !HFlow
        geometry: "0x0x0x{height}"
        padding: "{spacing}"
        children:
            - !Text
                geometry: "{label-width}x{height}"
                text: "{label}"
                alignment: CenterRight
            - !TextEntry
                geometry: "{entry-width}x{height}"
                pv: "{pv}"
                background: *edit_blue
```

The `!HFlow` arranges the label and entry field horizontally, and each instance
auto-sizes based on the provided dimensions.


## Nesting templates

Templates can instantiate other templates with `!Apply`:

```yaml
_MotorRow: !Template:MotorRow
    - !Defaults
        label-width: 120

    - !HFlow
        padding: 5
        children:
            - !Apply:PVReadWrite
                label: "{label}"
                label-width: "{label-width}"
                read-pv: "{motor-pv}.RBV"
                entry-pv: "{motor-pv}.VAL"
                units: "{units}"
```

The macro environment flows through to inner templates -- `{label}`, `{motor-pv}`,
and `{units}` are resolved from the outer apply context without needing to be explicitly
passed through.


## Conditional elements

Use `!If` and `!IfNot` to conditionally include elements based on whether a parameter
has a truthy value:

```yaml
_FlexRow: !Template:FlexRow
    - !Defaults
        read-pv: False
        entry-pv: False
        units: False

    - !HFlow
        padding: 5
        children:
            - !Text { geometry: "100x20", text: "{label}" }
            - !If:entry-pv
                - !TextEntry { geometry: "80x20", pv: "{entry-pv}" }
            - !If:read-pv
                - !TextMonitor { geometry: "80x20", pv: "{read-pv}" }
            - !If:units
                - !Text { geometry: "30x20", text: "{units}" }
```

The default value of `False` means the element is omitted unless the caller provides
a value. This is the pattern used throughout PVReadWrite -- each element only appears
when its parameter is set.


## Organizing templates in files

Templates are typically defined in their own `.yml` file and pulled in with `#include`:

```yaml
# my-templates.yml

#include colors.yml

_StatusIndicator: !Template:StatusIndicator
    # ...

_LabeledEntry: !Template:LabeledEntry
    # ...
```

```yaml
# layout.yml

#include colors.yml
#include my-templates.yml

Form: !Form
    title: "My Screen"

Row1: !Apply:StatusIndicator { pv: "$(P)Status" }
Row2: !Apply:LabeledEntry   { pv: "$(P)Setpoint", label: "SP:" }
```

Use the `--include` flag to add the directory containing your template files to the
search path:

```bash
python gestalt.py --include /path/to/templates --to ui layout.yml
```

Or place your template files alongside the layout file -- the layout's directory is
always searched first.


## Template design guidelines

1. **Provide sensible defaults** for everything except the primary PV parameter. Users
   should be able to get a working widget with minimal configuration.

2. **Use cascading defaults** (e.g., `element-width` flowing to `label-width`,
   `entry-width`, etc.) so users can control groups of properties with a single parameter.

3. **Use `False` as the default** for optional elements. This works with `!If` to
   cleanly omit unused sections.

4. **Prefix internal parameters** with the element name (e.g., `read-width`,
   `label-foreground`) to avoid naming collisions with outer templates.

5. **Keep templates focused**. A template that does one thing well is more reusable than
   one that tries to handle every case. Build complex screens by composing simple templates.

---

## Next steps

- [Conditional Elements](conditionals) -- Optionally show or hide elements with `!If` and `!IfNot`.
- [Overridable Defaults](embed-override) -- Let callers replace entire widgets using `!Embed`.
- [Template Reference](../reference/templates/) -- Documentation for Gestalt's built-in templates.
