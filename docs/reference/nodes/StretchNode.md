{% include header.md title='StretchNode' parent='Nodes' nav_order=29 %}
<a id="StretchNode"></a>

# StretchNode

A positioner used to stretch a widget to fill the space provided by its parent widget

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

