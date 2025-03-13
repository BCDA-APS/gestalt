---
layout: default
title: Positioners
parent: Nodes
grand_parent: Reference
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

Positioners are set up to be generated last among a set of unordered children nodes. This allows 
the rest of the nodes to expand the size of a parent widget before determining positioning. Be
careful though, as this does mean that the later generated widgets will appear above any other
widgets they share area with, despite being written in the stylesheet earlier. You can overwrite
this behavior by setting the "render-order" attribute to 0, but you may then have to define your
positioner node in a later part of the stylesheet in order for it to see the correct parent height
and width.

As well, it's important to note that this is only for unordered sets of children nodes. FlowNodes
will ignore this order and will place children nodes in the order they are defined in the template.


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


### AStrech

---

Determines a widget's width and height to match up respectively with the widget's parent values.

* **Example**

```yaml
Fill_Parent: !astretch:Text            
    text: "Middle"
    alignment: CenterLeft
```



### HStretch

---

Determines a widget's width to match up with the size of the widget's parent width.


* **Example**

```yaml
UITitle: !hstretch:Text
    geometry: 0x32
            
    text: "Middle"
    alignment: CenterLeft
```



### VStretch

---

Determines a widget's width to match up with the size of the widget's parent width.

You may also use the alias "stretch" to reference the vstretch node.


* **Example**

```yaml
UITitle: !vstretch:Text
    geometry: 32x0
            
    text: "Middle"
    alignment: CenterLeft
```



### HAnchor

---

Positions a widget at the horizontal extent of its parent node.


* **Example**

```yaml
WideGroup: !Group
    geometry: 400x20
    children:
        - !HAnchor:Text
            geometry: 50x20
            text: "I'm at the end"
```



### VAnchor

---

Positions a widget at the vertical extent of its parent node.

You may also use the alias "anchor" to reference the vachor node.


* **Example**

```yaml
TallGroup: !Group
    geometry: 40x200
    children:
        - !HAnchor:Text
            geometry: 50x20
            text: "I'm at the bottom"
```


### AAnchor

---

Positions a widget to be in the lower right corner of its parent node.


* **Example**

```yaml
BigGroup: !Group
    geometry: 400x400
    children:
        - !HAnchor:Text
            geometry: 50x20
            text: "I'm in the corner"
```
