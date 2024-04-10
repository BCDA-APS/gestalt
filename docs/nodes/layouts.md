---
layout: default
title: Layouts
parent: Nodes
nav_order: 3
---

# Layouts
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


### HFlow

---

Arranges children widgets along a horizontal axis. Each successive widget will have its
X position set such that it is a number of pixels away from the end of the previous widget
according to the value of the attribute `padding`. A widget's position on the Y axis is not
changed.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to space along the horizontal axis |
| padding      | Number | The number of pixels between each widget |
| background   | Color  | A fill color behind the entirety of all children |
| border-color | Color  | The color of the group's border surrounding the children widgets |
| border-width | Number | The thickness of the group's border in pixels |
| visibility   | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
CIO_Title: !hflow
    geometry: 0x2 x 0x0
    padding: 5
    
    children:
        - !Text { geometry: 70x20, text: "CIO 0-3" }
        - !TextMonitor
            geometry: 80x20
            background: *edit_blue
            foreground: *black
            
            pv: "$(P)CIOIn"
            
        - !Text { geometry: 90x20, text: "MIO 0-2" }
        - !TextMonitor
            geometry: 80x20
            background: *edit_blue
            foreground: *black
            
            pv: "$(P)MIOIn"
```

### VFlow

---

Arranges children widgets along a vertical axis. Each successive widget will have its
Y position set such that it is a number of pixels away from the end of the previous widget
according to the value of the attribute `padding`. A widget's position on the X axis is not
changed. 

You may also use the alias "flow" to reference the vflow node.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to space along the vertical axis |
| padding      | Number | The number of pixels between each widget |
| background   | Color  | A fill color behind the entirety of all children |
| border-color | Color  | The color of the group's border surrounding the children widgets |
| border-width | Number | The thickness of the group's border in pixels |
| visibility   | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
NumberedLED: !flow
    children:
        - !caLabel
            font: -Sans Serif - Regular - 8
            
            geometry: 50x15
            
            alignment: Qt::AlignHCenter|Qt::AlignVCenter
            fontScaleMode: ESimpleLabel::None
            
            text: "Input 1"
        
        - !caLed
            channel: !string "$(P)Bi1.VAL"
            trueColor: *alarm_red
            falseColor: *alarm_green
            
            borderColor: *transparent
            
            gradientEnabled: false
            
            geometry: 22x22
```


### HRepeat

---

Iterates over a given macro in the input file named by the attribute `repeat-over`, generating 
a copy of all children widgets as a group. Configures each such group according to the input 
macros and then positions the set of widgets along a horizontal axis. The group's starting X 
position is set such that it is a number of pixels away from the end of the previous widget 
group according to the value of the attribute `padding`. Widgets' positions on the Y axis are 
not changed.

If the macro named by `repeat-over` is parsed and found to be a number, then the node will iterate
a number of times specified by the macro. On each loop, the children widgets will be provided with
the macros `N` and `__index__` to use to configure themselves. `__index__` is a number that starts
at zero and increments by one every iteration of the loop. `N` is similar, but starts at a value
specified by the attribute `start-at`.

If, instead, `repeat-over` names a macro that is found to be a list of dictionaries, then the
dictionaries will be treated as the macros to use to configure the children widgets. The loop
will iterate over each of the specified mappings and will provide the children elements of the
group with those macros (alongside any other macros in the data file). The `__index__` macro
mentioned above will also be included.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to use as a template to copy along the horizontal axis |
| repeat-over  | String | The name of a macro that will be provided within the input data file |
| start-at     | Number | An offset value to the loop index to provide children widgets |
| padding      | Number | The number of pixels between each widget group |
| background   | Color  | A fill color behind the entirety of each template copy |
| border-color | Color  | The color of the group's border surrounding each template copy |
| border-width | Number | The thickness of the group's border in pixels |
| visibility   | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
UI_Row: !hrepeat
    repeat-over: "PLUGINS"
    
    geometry: 0x71 x 0x0
    
    padding: 6
    
    children:
        - !TextMonitor
            geometry: 10x1 x 110x18
            pv: "$(P){Instance}:PortName_RBV"
        
        - !RelatedDisplay            
            text: "More"
            
            geometry: 865x0 x 60x20
            
            links: 
                - { label: "{Instance}", file: "{Displays}", arg: "{Args}" }
```


### VRepeat

---

Iterates over a given macro in the input file named by the attribute `repeat-over`, generating 
a copy of all children widgets as a group. Configures each such group according to the input 
macros and then positions the set of widgets along a vertical axis. The group's starting Y 
position is set such that it is a number of pixels away from the end of the previous widget 
group according to the value of the attribute `padding`. Widgets' positions on the X axis are 
not changed.

If the macro named by `repeat-over` is parsed and found to be a number, then the node will iterate
a number of times specified by the macro. On each loop, the children widgets will be provided with
the macros `N` and `__index__` to use to configure themselves. `__index__` is a number that starts
at zero and increments by one every iteration of the loop. `N` is similar, but starts at a value
specified by the attribute `start-at`.

If, instead, `repeat-over` names a macro that is found to be a list of dictionaries, then the
dictionaries will be treated as the macros to use to configure the children widgets. The loop
will iterate over each of the specified mappings and will provide the children elements of the
group with those macros (alongside any other macros in the data file). The `__index__` macro
mentioned above will also be included.

You may also use the alias "repeat" to reference the vrepeat node.


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to use as a template to copy along the vertical axis |
| repeat-over  | String | The name of a macro that will be provided within the input data file |
| start-at     | Number | An offset value to the loop index to provide children widgets |
| padding      | Number | The number of pixels between each widget group |
| background   | Color  | A fill color behind the entirety of each template copy |
| border-color | Color  | The color of the group's border surrounding each template copy |
| border-width | Number | The thickness of the group's border in pixels |
| visibility   | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**


```yaml
UIRow: !repeat
    geometry: 0x20 x 0x0
    repeat-over: "NUM_CALCS"
        
    children:
        - !RelatedDisplay
            geometry: 0x0 x 25x20
            
            text: "{N}"
            
            foreground: *white
            background: *menu_green
            
            links:
                - { label: "user Calc {N}", file: "userCalc.ui", macros: "P=$(P),N={N},C=userCalc{N}" }
                - { label: "user Calc {N} (full)", file: "userCalc_full.ui", macros: "P=$(P),N={N},C=userCalc{N}" }
            
        - !ChoiceButton
            <<: *editable
            geometry: 25x0 x 40x20
            pv: "$(P)userCalc{N}Enable"
```



### Grid

---

Iterates over a given macro in the input file named by the attribute `repeat-over`, generating 
a copy of all children widgets as a group. Configures each such group according to the input 
macros and then positions the set of widgets in a grid pattern. The group's starting X and Y 
positions are set such that each group is a number of pixels away from the edges of any other 
group according to the value of the attribute `padding`. 

If the macro named by `repeat-over` is parsed and found to be a number, then the node will iterate
a number of times specified by the macro. On each loop, the children widgets will be provided with
the macros `N`, `__index__`, `__col__`, and `__row__` to use to configure themselves. `__index__` 
is a number that starts at zero and increments by one every iteration of the loop. `N` is similar, 
but starts at a value specified by the attribute `start-at`. `__row__` and `__col__` specify the
current 0-indexed position within the grid where the group will be generated.

If, instead, `repeat-over` names a macro that is found to be a list of dictionaries, then the
dictionaries will be treated as the macros to use to configure the children widgets. The loop
will iterate over each of the specified mappings and will provide the children elements of the
group with those macros (alongside any other macros in the data file). All the same macros
mentioned above will also be included.

The number of columns and rows in the node's grid pattern are determined by the number of iterations
specified by `repeat-over` combined with the attribute `aspect-ratio`. Defaulting to 1.0, `aspect-ratio` 
is the ratio between the number of columns to the number of rows to use. So an `aspect-ratio` of 2.0
would be specifying that the node should attempt to have twice as many columns as rows. This is
an idealized ratio and it may not be possible to exactly match the ratio as given with the number of
elements a user provides.


* **Special Attributes**

|      Name    |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to use as a template to copy in a grid pattern |
| repeat-over  | String | The name of a macro that will be provided within the input data file |
| start-at     | Number | An offset value to the loop index to provide children widgets |
| padding      | Number | The number of pixels between each widget group |
| aspect-ratio | Double | A ratio indicating the relative number of columns to the number of rows in the grid |
| background   | Color  | A fill color behind the entirety of each template copy |
| border-color | Color  | The color of the group's border surrounding each template copy |
| border-width | Number | The thickness of the group's border in pixels |
| horizontal   | Bool   | Fill direction of the layout. Macros will be mapped to widgets across columns first, then proceed to the next row, rather than the reverse. True by default |
| visibility   | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
LED_Grid: !Grid
    geometry: 160x170 x 0x0
    aspect-ratio: 1.5
    repeat-over: "LEDs"
    
    padding: 10

    children:
        - !LED
            <<: *alarm_led
            geometry: 20x20
```

