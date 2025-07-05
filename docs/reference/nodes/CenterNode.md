---
layout: default
title: CenterNode
parent: Nodes
nav_order: 6
has_toc: false
---


# CenterNode

A positioner used to place a widget centered within its parent's area

### ACenter

---

Positions a widget so that the midpoint of the widget matches up with the midpoint of the
widget's parent.

* **Example**

```yaml
MidPointGroup: !acenter:group    
    children:
        - !TextMontor
            geometry: 50x20
            foreground: *alarm_yellow
            background: *transparent
            alignment: CenterRight
            pv: "S:SRcurrentAI"
            
        - !Text
            geometry: 55x0 x 25x20
            foreground: *alarm_yellow
            alignment: CenterLeft
            text: "mA"
```



### HCenter

---

Positions a widget so that the midpoint of the widget on the horizontal axis matches up 
with the midpoint of the widget's parent on the same axis.

* **Example**

```yaml
OPSElements: !hcenter:group
    geometry: 0x7 x 0x0
    
    children:
        - !TextMontor
            geometry: 50x20
            foreground: *alarm_yellow
            background: *transparent
            alignment: CenterRight
            pv: "S:SRcurrentAI"
            
        - !Text
            geometry: 55x0 x 25x20
            foreground: *alarm_yellow
            alignment: CenterLeft
            text: "mA"
```


### VCenter

---

Positions a widget so that the midpoint of the widget on the vertical axis matches up 
with the midpoint of the widget's parent on the same axis.

You may also use the alias "center" to reference the vcenter node.


* **Example**

```yaml
OPSElements: !vcenter:group
    geometry: 7x0 x 0x0
    
    children:
        - !TextMonitor
            geometry: 0x0 x 50x20
            foreground: *alarm_yellow
            background: *transparent
            alignment: CenterRight
            pv: "S:SRcurrentAI"
            
        - !Text
            geometry: 55x0 x 25x20
            foreground: *alarm_yellow
            alignment: CenterLeft
            text: "mA"
```