---
layout: default
title: ScaleNode
parent: Nodes
nav_order: 25
has_toc: false
---


<a id="ScaleNode"></a>

# ScaleNode

A widget representing a bar filling up based on a pv's value versus its limits


* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| background   | Color     | Color of the unfilled portion of bar, $C9C9C9 by default |
| foreground   | Color     | Color of the filled portion of bar, $0000FF by default |
| horizontal   | Bool      | Whether to align the bar horizontally, defaults to False |
| pv           | String    | The PV being monitored |
| visibility   | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !Scale
    geometry: 0x0 x 50x200
    foreground: *burlywood
    pv: "xxx:yyy:zzz"
```

