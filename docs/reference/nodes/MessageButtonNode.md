---
layout: default
title: MessageButtonNode
parent: Nodes
nav_order: 19
has_toc: false
---


<a id="MessageButtonNode"></a>

# MessageButtonNode

A widget representing a button that writes a value to a pv when pressed

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| pv         | String | The PV that will be written to |
| value      | String | The value to write to the PV |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !MessageButton
    foreground: *black
    background: *edit_blue

    text: "Write Value"

    geometry: 10x200 x 100x20

    pv: "xxx:yyy:zzz"
    value: 1
```

