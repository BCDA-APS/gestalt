---
layout: default
title: RepeatNode
parent: Nodes
nav_order: 25
has_toc: false
---


# RepeatNode

A layout tool to repeat the same set of widgets along a given axis.

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
two macros; `__index__` and another that will be named according to `variable` so that the child 
widgets can configure themselves. `__index__` is a number that starts at zero and increments by 
one every iteration of the loop. The second macro is similar, but will start at a value specified 
by the attribute `start-at`.

If, instead, `repeat-over` names a macro that is found to be a list of dictionaries, then the
dictionaries will be treated as the macros to use to configure the children widgets. The loop
will iterate over each of the specified mappings and will provide the children elements of the
group with those macros (alongside any other macros in the data file). The `__index__` macro
mentioned above will also be included.

Finally, if `repeat-over` names a macro that is found to be a list of values, then the values will
be made available to each child under the name specified by the attribute `variable`. The `__index__` 
macro mentioned above will also be included.

* **Special Attributes**

|      Name      |  Type  | Description|
|----------------|--------|------------|
| children       | List   | A list of widgets to use as a template to copy along the horizontal axis |
| repeat-over    | String | The name of a macro that will be provided within the input data file |
| variable       | String | The name under which to provide the value of the loop index, 'N' by default |
| start-at       | Number | An offset value to the loop index to provide children widgets |
| padding        | Number | The number of pixels between each widget group |
| background     | Color  | A fill color behind the entirety of each template copy |
| border-color   | Color  | The color of the group's border surrounding each template copy |
| border-width   | Number | The thickness of the group's border in pixels |
| visibility     | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |
| ignore-empty   | Bool   | Defines whether or not to adjust positioning of elements if a repeated instance is an empty group. Useful for dealing with Conditional nodes. default: False |


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
<br>

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
two macros; `__index__` and another that will be named according to `variable` so that the child 
widgets can configure themselves. `__index__` is a number that starts at zero and increments by 
one every iteration of the loop. The second macro is similar, but will start at a value specified 
by the attribute `start-at`.

If, instead, `repeat-over` names a macro that is found to be a list of dictionaries, then the
dictionaries will be treated as the macros to use to configure the children widgets. The loop
will iterate over each of the specified mappings and will provide the children elements of the
group with those macros (alongside any other macros in the data file). The `__index__` macro
mentioned above will also be included.

Finally, if `repeat-over` names a macro that is found to be a list of values, then the values will
be made available to each child under the name specified by the attribute `variable`. The `__index__` 
macro mentioned above will also be included.

You may also use the alias "repeat" to reference the vrepeat node.


* **Special Attributes**

|      Name      |  Type  | Description|
|----------------|--------|------------|
| children       | List   | A list of widgets to use as a template to copy along the vertical axis |
| repeat-over    | String | The name of a macro that will be provided within the input data file |
| variable       | String | The name under which to provide the value of the loop index, 'N' by default |
| start-at       | Number | An offset value to the loop index to provide children widgets |
| padding        | Number | The number of pixels between each widget group |
| background     | Color  | A fill color behind the entirety of each template copy |
| border-color   | Color  | The color of the group's border surrounding each template copy |
| border-width   | Number | The thickness of the group's border in pixels |
| visibility     | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |
| ignore-empty   | Bool   | Defines whether or not to adjust positioning of elements if a repeated instance is an empty group. Useful for dealing with Conditional nodes. default: False |


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