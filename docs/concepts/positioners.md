---
layout: default
title: Positioners
parent: Concepts
nav_order: 3
---

# Positioners and Render Order
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

Positioner nodes (`!HStretch`, `!VCenter`, `!HAnchor`, etc.) modify a widget's
position or size relative to its parent container. Understanding how they interact
with layout containers is important for building screens that render correctly.


## How positioners work

A positioner is a prefix applied to another node's tag. It wraps the inner node and
adjusts its geometry after the inner node is generated:

- **Stretch** (`!HStretch`, `!VStretch`, `!AStretch`) -- Expands the widget to fill
  the parent's width, height, or both.
- **Center** (`!HCenter`, `!VCenter`) -- Centers the widget within the parent's width
  or height.
- **Anchor** (`!HAnchor`, `!VAnchor`, `!AAnchor`) -- Positions the widget at the far
  edge of the parent (right edge for horizontal, bottom edge for vertical).

All positioners read the parent's current dimensions to compute their result. A stretch
node reads the parent width to know how wide to make the widget. A center node reads
the parent center point to know where to place it.


## Render order in groups

Inside a `!Group`, positioners work reliably because groups use **render order** to
control when children are processed.

Regular widgets have render order 0. Positioner nodes have render order 1. The group
processes all render-order-0 children first, allowing its geometry to grow to
accommodate them. Then it processes render-order-1 children (the positioners), which
now see the group's final dimensions.

This means a `!HStretch:Text` inside a `!Group` will correctly stretch to the full
width of the group, even if other children were defined after it in the YAML file:

```yaml
Box: !Group
    geometry: 300x100
    children:
        - !HStretch:Text
            geometry: 0x30
            text: "Header"
            alignment: Center

        - !TextMonitor
            geometry: 10x40 x 200x20
            pv: "$(P)Value"
```

The header stretches to 300 pixels wide because the group's width is known before
the stretch node is resolved.


## The limitation with flow layouts

`!HFlow` and `!VFlow` process children in **insertion order** (the order they appear
in the YAML file), not by render order. This is necessary because position in a flow
is sequential -- each child's position depends on the cumulative size of all previous
children.

However, this means that a positioner placed early in a flow may not see the flow's
final dimensions. The flow's geometry grows as children are added, so a stretch node
at the top of a flow would stretch to whatever the flow's width was at that point
(possibly zero), not the final width after all children are placed.

```yaml
# This will NOT work as expected
Content: !VFlow
    padding: 5
    children:
        - !HStretch:Text           # Resolved first, flow width may be 0
            geometry: 0x30
            text: "Header"
        - !TextMonitor             # Resolved second, flow grows to fit
            geometry: 200x20
            pv: "$(P)Value"
```

The header would not stretch to 200 pixels because the flow hadn't processed the
TextMonitor yet when the stretch was resolved.


## Recommended patterns

### Top-level stretch nodes

Place stretch nodes as top-level entries in the layout, not inside a flow. Top-level
nodes stretch relative to the screen (Form) width, which is always known:

```yaml
Header: !HStretch:Text
    geometry: 0x30
    text: "Device Control"
    font: -Cantarell - Bold
    foreground: *white
    background: *header_blue
    alignment: Center

Controls: !VFlow
    geometry: 0x35 x 0x0
    padding: 5
    children:
        - !Apply:PVReadWrite { label: "Setpoint:", entry-pv: "$(P)Set" }
        - !Apply:PVReadWrite { label: "Mode:",     menu-pv: "$(P)Mode" }
```

The header stretches to the screen width. The VFlow starts at Y=35 to sit below it.
This is the pattern used by `ScreenHeader`.

### Positioners inside groups

When you need a positioner inside a container, use a `!Group` with explicit geometry
instead of a flow:

```yaml
Panel: !Group
    geometry: 300x200
    children:
        - !HStretch:Text
            geometry: 0x30
            text: "Panel Title"
            alignment: Center

        - !VFlow
            geometry: 0x35 x 0x0
            padding: 5
            children:
                - !TextMonitor { geometry: 200x20, pv: "$(P)Val1" }
                - !TextMonitor { geometry: 200x20, pv: "$(P)Val2" }
```

The stretch node is a child of the group (which uses render order), not the flow.

### VCenter inside HFlow

`!VCenter` inside an `!HFlow` is a common and safe pattern. PVReadWrite uses it
extensively:

```yaml
Row: !HFlow
    padding: 5
    children:
        - !VCenter:Text { geometry: 100x20, text: "Label:" }
        - !VCenter:TextEntry { geometry: 80x20, pv: "$(P)Value" }
```

This works because `!VCenter` adjusts vertical position, not horizontal, and the
HFlow's height grows as children are placed. Each VCenter node gets a second pass
to adjust its vertical position after being placed.

---

## Next steps

- [Core Concepts](./#nodes) -- Overview of node categories including positioners.
- [Architecture](architecture) -- How the node tree is processed during generation.
