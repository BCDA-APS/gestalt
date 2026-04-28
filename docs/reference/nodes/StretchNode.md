---
layout: default
title: StretchNode
parent: Nodes
nav_order: 30
has_toc: false
---


# StretchNode

A positioner used to stretch a widget to fill the space provided by its parent widget

### AStretch

---

Determines a widget's width and height to match up respectively with the widget's parent values.

* **Example**

```yaml
Fill_Parent: !AStretch:TextMonitor
    foreground: *white
    alignment: Center
    pv: "$(P)$(R).DESC"
```



### HStretch

---

Determines a widget's width to match up with the size of the widget's parent width.


* **Example**

```yaml
ScreenTitle: !HStretch:Text
    geometry: 0x0 x 0x45
    foreground: *white
    background: *header_blue
    border-color: *black
    border-width: 3
    text: "Screen Title"
    font: "-Liberation Sans -Bold -16"
    alignment: Center
```



### VStretch

---

Determines a widget's height to match up with the size of the widget's parent height.

You may also use the alias "stretch" to reference the vstretch node.


* **Example**

```yaml
SideIndicator: !VStretch:Rectangle
    geometry: 8x0
    background: *alarm_red
    border-color: *transparent
```