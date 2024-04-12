---
layout: default
title: Positioners
parent: Nodes
nav_order: 4
---

# Positioners
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


<br>

Positioners are special tags that can be applied to a widget type which overwrite the
geometry of the given widget when the output file is written. All other attributes of
the widget are defined as normal and not touched by the positioner.

When defining the widget you want to position, just prepend with widget's type with the
positioner's type. So if you have a Text widget, which is normally indicated with the '!Text'
type, and you want to horizontally center it within its parent, you would change that type
to '!hcenter:Text'.



### ACenter

---

Positions a widget so that the midpoint of the widget matches up with the midpoint of the
widget's parent. Note that, a parent's size is determined at the point when a widget is 
defined. Any widgets defined afterward may affect the final size of the parent.

* **Example**

```yaml
MidPointGroup: !acenter:group    
    children:
        - !TextMontor
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



### HCenter

---

Positions a widget so that the midpoint of the widget on the horizontal axis matches up 
with the midpoint of the widget's parent on the same axis. Note that, a parent's size is 
determined at the point when a widget is defined. Any widgets defined afterward may affect 
the final size of the parent.

* **Example**

```yaml
OPSElements: !hcenter:group
    geometry: 0x7 x 0x0
    
    children:
        - !TextMontor
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


### VCenter

---

Positions a widget so that the midpoint of the widget on the vertical axis matches up 
with the midpoint of the widget's parent on the same axis. Note that, a parent's size 
is determined at the point when a widget is defined. Any widgets defined afterward may 
affect the final size of the parent.

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


### AStrech

---

Determines a widget's width and height to match up respectively with the widget's parent values.
Note that, a parent's size is determined at the point when a widget is defined. Any
widgets defined afterward may affect the final size of the parent.

* **Example**

```yaml
Fill_Parent: !astretch:Text            
    text: "Middle"
    alignment: CenterLeft
```



### HStretch

---

Determines a widget's width to match up with the size of the widget's parent width.
Note that, a parent's size is determined at the point when a widget is defined. Any
widgets defined afterward may affect the final size of the parent.


* **Example**

```yaml
UITitle: !hstretch:Text
    geometry: 0x0 x 0x32
            
    text: "Middle"
    alignment: CenterLeft
```



### VStretch

---

Determines a widget's width to match up with the size of the widget's parent width.
Note that, a parent's size is determined at the point when a widget is defined. Any
widgets defined afterward may affect the final size of the parent.

You may also use the alias "stretch" to reference the vstretch node.


* **Example**

```yaml
UITitle: !vstretch:Text
    geometry: 0x0 x 32x0
            
    text: "Middle"
    alignment: CenterLeft
```
