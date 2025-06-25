---
layout: default
title: MenuNode
parent: Nodes
nav_order: 17
has_toc: false
---


<a id="MenuNode"></a>

# MenuNode

A widget representing a menu that gets its options from an enumerable pv


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| pv         | String | The PV containing the enumerable value |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !Menu
    foreground: *black
    background: *edit_blue
    geometry: 355x0 x 80x20
    pv: $(P){Instance}:EnableCallbacks
```

