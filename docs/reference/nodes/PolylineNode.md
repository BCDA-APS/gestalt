---
layout: default
title: PolylineNode
parent: Nodes
nav_order: 21
has_toc: false
---


<a id="PolylineNode"></a>

# PolylineNode

A set of contiguous line segments


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| border-color | Color  | Widget line color, $000000 by default |
| border-width | Number | Thickness of widget outline, 2 by default |
| points       | List   | A list of Rect's representing the contiguous points of the polyline |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
Star: !PolyLine
    geometry: 40x40
    points: [ 20x0, 0x40, 40x10, 0x10, 40x40, 20x0 ]
```

