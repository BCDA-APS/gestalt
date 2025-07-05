---
layout: default
title: TextEntryNode
parent: Nodes
nav_order: 33
has_toc: false
---


# TextEntryNode

A widget representing a text entry field.

* **Special Attributes**

|    Name    |    Type   | Description|
|------------|-----------|------------|
| geometry   | Rect      | A rectangle describing the position and dimensions of the widget |
| foreground | Color     | Widget foreground color |
| background | Color     | Widget background color |
| font       | Font      | Widget display font |
| alignment  | Alignment | Display text alignment |
| format     | String    | Text display format, value is one of "String, Decimal, Engineering, Exponential, Compact, Hexadecimal, Binary" |
| pv         | String    | The PV that will be written to |
| visibility | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !TextEntry
    geometry: 5x0 x 120x20
    
    pv: "$(P)$(R)Description"
    
    alignment: BottomLeft
```