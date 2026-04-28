---
layout: default
title: FlowNode
parent: Nodes
nav_order: 11
has_toc: false
---


# FlowNode

A layout tool to place widgets along a given axis, one after another.

### HFlow

---

Arranges children widgets along a horizontal axis. Each successive widget will have its
X position set such that it is a number of pixels away from the end of the previous widget
according to the value of the attribute `padding`. A widget's position on the Y axis is not
changed.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to space along the horizontal axis |
| padding      | Number | The number of pixels between each widget |
| background   | Color  | A fill color behind the entirety of all children |
| border-color | Color  | The color of the group's border surrounding the children widgets |
| border-width | Number | The thickness of the group's border in pixels |
| visibility   | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
ReadbackRow: !HFlow
    geometry: 0x2 x 0x0
    padding: 5
    
    children:
        - !Text { geometry: 70x20, text: "Input 1" }
        - !TextMonitor
            geometry: 80x20
            background: *edit_blue
            foreground: *black
            pv: "$(P)$(R)Input1"
            
        - !Text { geometry: 70x20, text: "Input 2" }
        - !TextMonitor
            geometry: 80x20
            background: *edit_blue
            foreground: *black
            pv: "$(P)$(R)Input2"
```

<br>

### VFlow

---

Arranges children widgets along a vertical axis. Each successive widget will have its
Y position set such that it is a number of pixels away from the end of the previous widget
according to the value of the attribute `padding`. A widget's position on the X axis is not
changed. 

You may also use the alias "flow" to reference the vflow node.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to space along the vertical axis |
| padding      | Number | The number of pixels between each widget |
| background   | Color  | A fill color behind the entirety of all children |
| border-color | Color  | The color of the group's border surrounding the children widgets |
| border-width | Number | The thickness of the group's border in pixels |
| visibility   | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
StatusColumn: !VFlow
    padding: 5
    
    children:
        - !Text
            geometry: 80x20
            text: "Status"
            alignment: Center
            
        - !LED
            geometry: 20x20
            pv: "$(P)$(R)Status_RBV"
            true-color: *alarm_green
            false-color: *grey_dark
            
        - !TextMonitor
            geometry: 80x20
            foreground: *header_blue
            pv: "$(P)$(R)Value_RBV"
```