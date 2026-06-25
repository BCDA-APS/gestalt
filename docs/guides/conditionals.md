---
layout: default
title: Conditional Elements
parent: Guides
nav_order: 5
---

# Conditional Elements
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

`!If` and `!IfNot` let you conditionally include elements in a template based on
whether a parameter has a truthy value. This is how templates create optional elements
that only appear when the caller provides a value for them.


## Basic usage

`!If:parameter-name` includes its children only when the named parameter is truthy
(not `False`, not `0`, not empty). `!IfNot:parameter-name` does the inverse.

```yaml
_StatusRow: !Template:StatusRow
    - !Defaults
        label: "Status"
        units: False

    - !HFlow
        padding: 5
        children:
            - !Text        { geometry: "100x20", text: "{label}" }
            - !TextMonitor { geometry: "80x20",  pv: "{pv}" }
            - !If:units
                - !Text    { geometry: "30x20",  text: "{units}" }
```

When called without `units`, the text widget is omitted:

```yaml
# No units shown
Temp: !Apply:StatusRow
    pv: "$(P)Temp:RBV"
    label: "Temperature"

# Units shown
Pressure: !Apply:StatusRow
    pv: "$(P)Pres:RBV"
    label: "Pressure"
    units: "psi"
```

The key technique is defaulting the parameter to `False` in the `!Defaults` block.
`!If` treats `False` as falsy, so the element is hidden unless the caller overrides it
with an actual value.


## Inline conditional syntax

For simple cases, `!If` supports an inline list syntax that keeps the layout compact:

```yaml
- !If:units [ !Text { geometry: "30x20", text: "{units}" } ]
```

This is equivalent to the multi-line form but fits on a single line. You can include
multiple widgets in the list:

```yaml
- !If:read-pv [ !TextMonitor { geometry: "80x20", pv: "{read-pv}" }, !Spacer { geometry: "10x0" } ]
```


## Conditional PV elements

The most common pattern is using a PV name as the conditional. When the PV parameter
is `False` (the default), the element is hidden. When the caller provides a PV string,
the element appears:

```yaml
_FlexRow: !Template:FlexRow
    - !Defaults
        entry-pv: False
        read-pv:  False
        menu-pv:  False

    - !HFlow
        padding: 5
        children:
            - !Text { geometry: "100x20", text: "{label}" }
            - !If:entry-pv [ !TextEntry  { geometry: "80x20", pv: "{entry-pv}" } ]
            - !If:menu-pv  [ !Menu       { geometry: "80x20", pv: "{menu-pv}" } ]
            - !If:read-pv  [ !TextMonitor { geometry: "80x20", pv: "{read-pv}" } ]
```

Callers enable only the elements they need:

```yaml
# Entry + readback
SetpointRow: !Apply:FlexRow
    label: "Setpoint:"
    entry-pv: "$(P)Setpoint"
    read-pv:  "$(P)Setpoint:RBV"

# Menu only
ModeRow: !Apply:FlexRow
    label: "Mode:"
    menu-pv: "$(P)Mode"
```

This is the core pattern used by `PVReadWrite` -- each of its many elements (label,
entry, menu, button, choice, readback, units, LED, enable) defaults to `False` and
only appears when a value is provided.


## Spacing with conditionals

When using conditionals inside a flow layout, put the spacer inside the conditional
so it only appears when the element is visible:

```yaml
- !If:read-pv [ !TextMonitor { geometry: "80x20", pv: "{read-pv}" }, !Spacer { geometry: "10x0" } ]
- !If:menu-pv [ !Menu { geometry: "80x20", pv: "{menu-pv}" }, !Spacer { geometry: "10x0" } ]
```

If the spacer were outside the conditional, you would get extra gaps where hidden
elements should have been.


## Using !IfNot

`!IfNot` is the inverse of `!If` -- it includes children when the parameter is falsy.
This is useful for switching between two variants of a widget based on a configuration
flag:

```yaml
- !If:read-only
    - !TextMonitor { geometry: "80x20", pv: "{pv}" }
- !IfNot:read-only
    - !TextEntry { geometry: "80x20", pv: "{pv}" }
```

With `read-only: true`, the caller gets a read-only monitor. Without it (or with
`read-only: false`), they get an editable entry field.


## Conditionals with read-first

`PVReadWrite` uses a combination of `!If` and `!IfNot` on the same parameter to
place elements in different positions depending on a boolean flag:

```yaml
# Readback before entry fields
- !If:read-first
    - !If:read-pv [ !TextMonitor { ... } ]
    - !If:units   [ !Text { ... } ]

# Entry fields here...

# Readback after entry fields (the default)
- !IfNot:read-first
    - !If:read-pv [ !TextMonitor { ... } ]
    - !If:units   [ !Text { ... } ]
```

The same elements appear in both branches, but their position in the flow changes
based on the `read-first` flag.

---

## Next steps

- [Overridable Elements](embed-override) -- Let callers replace entire widgets using `!Embed`.
- [Custom Templates](custom-templates) -- Fundamentals of writing templates.
- [ConditionalNode Reference](../reference/nodes/ConditionalNode) -- Full node documentation.
