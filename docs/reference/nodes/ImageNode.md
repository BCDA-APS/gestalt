---
layout: default
title: ImageNode
parent: Nodes
nav_order: 14
has_toc: false
---


<a id="ImageNode"></a>

# ImageNode

A widget that displays a given image file


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| file       | String | The filepath of the image to display |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
ComplicatedStructure: !Image
    file: "/path/to/image/Beamline.png"
```

