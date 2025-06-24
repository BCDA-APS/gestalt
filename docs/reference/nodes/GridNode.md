{% include header.md title='GridNode' parent='Nodes' nav_order=12 %}
<a id="GridNode"></a>

# GridNode

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

You can also control the shape by specifying the minimum and maximum numbers of columns and rows. Using
'min-cols', 'max-cols', 'min-rows', and 'max-rows', you can restrict the automatic shaping done based
off of 'aspect-ratio'. If there is a conflict between the number of iterations, the aspect-ratio, and
the minimum/maximum values, then the 'horizontal' attribute will be used to determine which restrictions
to weight heavier. If 'horizontal' is True, then size will break any horizontal constraints (adding additional
columns). If 'horizontal' is False, then the vertical constraints will be broken (adding additional rows).


* **Special Attributes**

|       Name     |  Type  | Description|
|----------------|--------|------------|
| children       | List   | A list of widgets to use as a template to copy in a grid pattern |
| repeat-over    | String | The name of a macro that will be provided within the input data file |
| variable       | String | The name under which to provide the value of the loop index, 'N' by default |
| start-at       | Number | An offset value to the loop index to provide children widgets |
| padding        | Number | The number of pixels between each widget group |
| aspect-ratio   | Double | A ratio indicating the relative number of columns to the number of rows in the grid |
| background     | Color  | A fill color behind the entirety of each template copy |
| border-color   | Color  | The color of the group's border surrounding each template copy |
| border-width   | Number | The thickness of the group's border in pixels |
| horizontal     | Bool   | Fill direction of the layout. Macros will be mapped to widgets across columns first, then proceed to the next row, rather than the reverse. True by default |
| visibility     | String | A pv that determines the visibility of the layout, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |
| ignore-empty   | Bool   | Defines whether or not to adjust positioning of elements if a repeated instance is an empty group. Useful for dealing with Conditional nodes. default: False |


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

