{% include header.md title='AnchorNode' parent='Nodes' nav_order=1 %}
<a id="AnchorNode"></a>

# AnchorNode

A positioner used to place a widget along the edge of its parents area

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

