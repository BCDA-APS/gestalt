---
layout: default
title: ChoiceButtonNode
parent: Nodes
nav_order: 7
has_toc: false
---


# ChoiceButtonNode

A widget representing a set of buttons that gets its options from an enumerable pv

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| selected   | Color  | Selected item color, defaults to background color |
| font       | Font   | Widget display font |
| pv         | String | The PV containing the enumerable value |
| horizontal | Bool   | Whether to arrange the buttons horizontally, defaults to True |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
OnOff: !ChoiceButton
    geometry: 215x20
    
    pv: "$(P)userCalcEnable.VAL"
    foreground: *black
    background: *edit_blue
```