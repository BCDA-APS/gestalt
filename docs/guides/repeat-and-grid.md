---
layout: default
title: Data-Driven Layouts
parent: Guides
nav_order: 8
---

# Data-Driven Layouts
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

Repeat and Grid nodes generate multiple copies of their children from input data.
`!HRepeat` and `!VRepeat` arrange copies along a single axis. `!Grid` arranges them
in a two-dimensional grid.


## How repeat-over works

All repeat and grid nodes use the `repeat-over` attribute to determine what to iterate
over. The value can be provided in several ways:

- **A literal value** -- `repeat-over: 4`
- **A macro name** -- `repeat-over: COUNT` (looked up in the data environment)
- **A macro reference** -- `repeat-over: "{COUNT}"`
- **An inline list** -- `repeat-over: [ "A", "B", "C" ]`

After resolution, the final value determines the iteration behavior:

- A **number** -- repeat that many times.
- A **list of values** -- repeat once per value.
- A **list of dictionaries** -- repeat once per dictionary, unpacking each dict's
  keys as macros.

On every iteration, two macros are always available to children:

- **`{__index__}`** -- A zero-based counter that increments by one each iteration,
  regardless of `start-at` or `increment`.
- **`{N}`** (or whatever `variable` is set to) -- The iteration value. What this
  contains depends on the type of data being iterated over, as described below.


## Repeating a number of times

When `repeat-over` resolves to a number, the node iterates that many times. The
`variable` macro (default `{N}`) receives a computed index value controlled by
`start-at` and `increment`:

```yaml
Indicators: !VRepeat
    repeat-over: "COUNT"
    padding: 5
    children:
        - !LED { geometry: 20x20, pv: "$(P)Status{N}" }
```

With input data `COUNT: 4`, this produces four LEDs. By default, `{N}` takes values
`0, 1, 2, 3` and `{__index__}` takes the same values `0, 1, 2, 3`.

### Changing the start value

`start-at` offsets the value of `{N}` without affecting `{__index__}`:

```yaml
Motors: !VRepeat
    repeat-over: "MOTORS"
    start-at: 1
    padding: 5
    children:
        - !Text { geometry: 100x20, text: "Motor {N}" }
```

With `MOTORS: 4`, `{N}` takes values `1, 2, 3, 4` while `{__index__}` is still
`0, 1, 2, 3`.

### Changing the increment

`increment` controls the step size for `{N}`:

```yaml
EvenChannels: !VRepeat
    repeat-over: "COUNT"
    start-at: 0
    increment: 2
    padding: 5
    children:
        - !Text { geometry: 100x20, text: "Channel {N}" }
```

With `COUNT: 4`, `{N}` takes values `0, 2, 4, 6`.


## Repeating over a list of values

When `repeat-over` resolves to a list of scalar values, the node iterates once per
item. The `variable` macro receives each value in turn:

```yaml
Names: !HRepeat
    repeat-over: "LABELS"
    variable: "name"
    padding: 10
    children:
        - !Text { geometry: 80x20, text: "{name}" }
```

With input data:

```yaml
LABELS: ["Alice", "Bob", "Charlie"]
```

This produces three labels. `{name}` takes the values `"Alice"`, `"Bob"`, `"Charlie"`.
`{__index__}` takes `0, 1, 2`.

The `variable` attribute controls the macro name -- here `{name}` instead of the
default `{N}`.

### Inline lists

Lists can be defined directly in the layout instead of coming from a data file:

```yaml
Buttons: !HRepeat
    repeat-over: [ "Start", "Stop", "Reset" ]
    variable: "action"
    padding: 5
    children:
        - !MessageButton
            geometry: 80x30
            text: "{action}"
            pv: "$(P){action}"
            value: 1
```


## Repeating over a list of dictionaries

When `repeat-over` resolves to a list of dictionaries, each dictionary's keys are
unpacked directly into the macro environment for that iteration. This is the most
powerful form:

```yaml
Rows: !VRepeat
    repeat-over: "CHANNELS"
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "{label}:"
            entry-pv: "$(P){pv}:Set"
            read-pv:  "$(P){pv}:RBV"
```

With input data:

```yaml
CHANNELS:
    - { label: "Temperature", pv: "Temp" }
    - { label: "Pressure",    pv: "Pres" }
    - { label: "Flow Rate",   pv: "Flow" }
```

Each iteration gets `{label}` and `{pv}` from its corresponding dictionary. The
index `{__index__}` is still available (`0, 1, 2`), and `{N}` receives the entire
dictionary object (though referencing the individual keys directly is more common).

Inline lists of dictionaries work the same way:

```yaml
MotorControls: !HRepeat
    padding: 10
    repeat-over:
        - { group: "h", motor: "Center" }
        - { group: "h", motor: "Size" }
        - { group: "v", motor: "Center" }
        - { group: "v", motor: "Size" }

    children:
        - !VFlow
            padding: 5
            children:
                - !Text { geometry: 160x28, text: "{motor}", alignment: Center }
                - !TextMonitor { geometry: 160x20, pv: "$(P)$(SLITS):{group}{motor}.RBV" }
```


## Horizontal vs vertical

`!HRepeat` arranges copies along the horizontal axis. `!VRepeat` (or the alias
`!Repeat`) arranges them vertically. The `padding` attribute controls the gap between
copies in both cases.


## Grid layout

`!Grid` arranges repeated children in a two-dimensional grid. It uses `aspect-ratio`
to determine the number of columns relative to rows:

```yaml
LEDGrid: !Grid
    repeat-over: "NUM_LEDS"
    aspect-ratio: 2.0
    padding: 5
    children:
        - !LED { geometry: 20x20, pv: "$(P)LED{N}" }
```

With `NUM_LEDS: 12` and `aspect-ratio: 2.0`, this produces a grid that is roughly
twice as wide as it is tall (e.g., 4 columns by 3 rows).

The `repeat-over` attribute works identically to repeat nodes -- numbers, lists, and
lists of dictionaries are all supported.

### Grid-specific macros

Inside a grid, children have access to two additional macros beyond `{N}` and
`{__index__}`:

- `{__col__}` -- the current column (0-indexed)
- `{__row__}` -- the current row (0-indexed)

### Fill direction

By default, the grid fills horizontally (left to right, then next row). Set
`horizontal: false` to fill vertically (top to bottom, then next column):

```yaml
VerticalGrid: !Grid
    repeat-over: "COUNT"
    aspect-ratio: 0.5
    horizontal: false
    padding: 5
    children:
        - !Text { geometry: 60x20, text: "Item {N}" }
```


## Tabbed repeat

`!TabbedRepeat` combines a tabbed display with repeat iteration. Each iteration
produces a new tab containing a copy of the children widgets:

```yaml
ChannelTabs: !TabbedRepeat
    geometry: 400x300
    repeat-over: "CHANNELS"
    variable: "ch"

    tab-color: *header_blue
    foreground: *white
    selected: $3970C4
    border-color: *header_blue
    font: -DejaVu Sans Mono - Bold - 9

    children:
        - !VFlow
            padding: 5
            children:
                - !TextMonitor { geometry: 120x20, pv: "$(P)$(R){ch}:Value_RBV" }
                - !TextEntry   { geometry: 120x20, pv: "$(P)$(R){ch}:Setpoint", background: *edit_blue }
```

Tab names are set from `{__index__}` (the 0-based iteration counter), so tabs for a
list of 4 items would be labeled `0`, `1`, `2`, `3`.

The same `repeat-over` modes are supported: numbers, lists of values, and lists of
dictionaries. Tab-specific styling attributes include `tab-color`, `selected` (the
active tab color), `foreground`, `font`, `border-color`, `inset` (horizontal offset
of the tab bar), and `offset` (vertical gap between tabs and content).


## Reversing the order

Set `reverse: true` on any repeat or grid node to iterate in reverse order:

```yaml
Channels: !VRepeat
    repeat-over: "NUM"
    start-at: 1
    reverse: true
    padding: 5
    children:
        - !Text { geometry: 100x20, text: "Ch {N}" }
```

With `NUM: 3`, this produces rows for Ch 3, Ch 2, Ch 1.


## Handling empty iterations

When using conditionals inside a repeat, some iterations may produce no visible
widgets. By default, empty iterations still take up space. Set `ignore-empty: true`
to collapse the gap:

```yaml
FilteredList: !VRepeat
    repeat-over: "ITEMS"
    padding: 5
    ignore-empty: true
    children:
        - !If:enabled
            - !Text { geometry: 100x20, text: "{label}" }
```

---

## Next steps

- [RepeatNode Reference](../reference/nodes/RepeatNode) -- Full attribute reference for HRepeat and VRepeat.
- [GridNode Reference](../reference/nodes/GridNode) -- Full attribute reference for Grid.
- [TabbedRepeatNode Reference](../reference/nodes/TabbedRepeatNode) -- Full attribute reference for TabbedRepeat.
- [Using Data Files](data-files) -- How to provide input data in different formats.
