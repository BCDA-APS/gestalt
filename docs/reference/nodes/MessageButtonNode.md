---
layout: default
title: MessageButtonNode
parent: Nodes
nav_order: 19
has_toc: false
---


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


* **Examples**

```yaml
StopButton: !MessageButton
    geometry: 140x26
    background: *alarm_red
    foreground: *alarm_yellow
    text: "STOP"
    pv: "$(P)$(M).STOP"
    value: 1
```

Message buttons are often used in pairs for open/close or enable/disable controls:

```yaml
- !MessageButton
    geometry: 100x25
    background: $006400
    foreground: $FFFFFF
    text: "Open"
    pv: "$(P)$(R)State"
    value: 0

- !MessageButton
    geometry: 100x25
    background: $8B0000
    foreground: $FFFFFF
    text: "Close"
    pv: "$(P)$(R)State"
    value: 1
```