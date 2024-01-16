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


### hcenter

---

Positions a widget so that the midpoint of the widget on the horizontal axis matches up 
with the midpoint of the widget's parent on the same axis. Note that, a parent's size is 
determined at the point when a widget is defined. Any widgets defined afterward may affect 
the final size of the parent.


* **Special Attributes**

Positioners don't have attributes, their only internal element should be whatever node
is being positioned.


* **Example**

```yaml
Centering: !hcenter
    OPSElements: !group
        geometry: 0x7 x 0x0
        
        children:
            - !caLineEdit
                geometry: 0x0 x 50x20
                foreground: *alarm_yellow
                background: *transparent
                colorMode: caLineEdit::Static
                alignment: Qt::AlignRight|Qt::AlignVCenter
                channel: "S:SRcurrentAI"
                
            - !caLabel
                geometry: 55x0 x 25x20
                foreground: *alarm_yellow
                alignment: Qt::AlignLeft|Qt::AlignVCenter
                text: "mA"
```


### vcenter

---

Positions a widget so that the midpoint of the widget on the vertical axis matches up 
with the midpoint of the widget's parent on the same axis. Note that, a parent's size 
is determined at the point when a widget is defined. Any widgets defined afterward may 
affect the final size of the parent.

You may also use the alias "center" to reference the vcenter node.


* **Special Attributes**

Positioners don't have attributes, their only internal element should be whatever node
is being positioned.


* **Example**

```yaml
Centering: !vcenter
    OPSElements: !group
        geometry: 7x0 x 0x0
        
        children:
            - !caLineEdit
                geometry: 0x0 x 50x20
                foreground: *alarm_yellow
                background: *transparent
                colorMode: caLineEdit::Static
                alignment: Qt::AlignRight|Qt::AlignVCenter
                channel: "S:SRcurrentAI"
                
            - !caLabel
                geometry: 55x0 x 25x20
                foreground: *alarm_yellow
                alignment: Qt::AlignLeft|Qt::AlignVCenter
                text: "mA"
```


### hstretch

---

Determines a widget's width to match up with the size of the widget's parent width.
Note that, a parent's size is determined at the point when a widget is defined. Any
widgets defined afterward may affect the final size of the parent.

* **Special Attributes**

Positioners don't have attributes, their only internal element should be whatever node
is being positioned.


* **Example**

```yaml
StretchOut: !hstretch
    UITitle: !caLabel
        geometry: 0x0 x 0x32
                
        text: "Middle"
        alignment: Qt::AlignLeft|Qt::AlignVCenter
```



### vstretch

---

Determines a widget's width to match up with the size of the widget's parent width.
Note that, a parent's size is determined at the point when a widget is defined. Any
widgets defined afterward may affect the final size of the parent.

You may also use the alias "stretch" to reference the vstretch node.


* **Special Attributes**

Positioners don't have attributes, their only internal element should be whatever node
is being positioned.


* **Example**

```yaml
StretchOut: !vstretch
    UITitle: !caLabel
        geometry: 0x0 x 32x0
                
        text: "Middle"
        alignment: Qt::AlignLeft|Qt::AlignVCenter
```
