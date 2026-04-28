---
layout: default
title: GroupNode
parent: Nodes
nav_order: 13
has_toc: false
---


# GroupNode

A container widget that holds children elements within a bordered, optionally filled area.

Groups serve as the basic building block for organizing widgets. Children are
positioned relative to the group's origin, offset by the group's margins and
border width. The group automatically grows to fit its children.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| children     | List   | A list of child widgets contained by this group |
| background   | Color  | A fill color for the group, defaults to transparent |
| border-color | Color  | The color of the group's border, defaults to $000000 |
| border-width | Number | The thickness of the group's border in pixels, defaults to 0 |
| margins      | Rect   | Inset spacing within the group's border, defaults to 0x0x0x0 |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
StatusBox: !Group
    geometry: 200x100
    background: $EEEEEE
    border-width: 2
    border-color: *black
    margins: 5x5x5x5
    
    children:
        - !Text
            geometry: 0x0 x 190x20
            text: "Device Status"
            alignment: Center
            
        - !TextMonitor
            geometry: 0x25 x 190x20
            pv: "$(P)$(R)Status_RBV"
```

Groups can also be used as visibility containers, showing or hiding
their children based on a PV value:

```yaml
ConditionalControls: !Group
    visibility: "$(P)$(R)Enabled"
    children:
        - !MessageButton
            geometry: 100x30
            text: "Start"
            pv: "$(P)$(R)Start"
            value: 1
```