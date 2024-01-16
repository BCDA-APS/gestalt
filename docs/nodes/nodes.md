---
layout: default
title: Nodes
nav_order: 3
has_children: true
---

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}



## Nodes

The default element underlying the generation of any output files in Gestalt is
the Node. When a template file is parsed, it is turned into a graph of these Nodes.
Providing the graph with a set of input data and traversing the Nodes is then used
to construct the proper output.

There are four major categories of Nodes; Widgets, Logical Groups, Layouts, and 
Positioners. Nodes contain a set of attribute data describing their configuration and 
the logic of how to apply those attributes to a given output data format.


## Widgets

Currently, the way that widgets are supported is by directly interfacing with the
widget types of each of the output formats. Widget Nodes are created by giving the
widget name of the caQtDM or CSS widget that will be created and then specifying
attributes with names and values equivalent to the names and values within their
equivalent designer programs. Further information about this is described in the 
[Templates](templates.md) section.

Eventually, a set of output-independent widgets will be created with their own 
property naming convention that will be capable of converting such properties into
the correct attributes in both caQtDM and CSS.


## Logical Groups

Logical groups perform some form of calculation upon their children widgets. Currently,
the only logical group used is the '!conditional' type. A conditional group uses a 
boolean value to decide whether to add their contents to the screen or not. Within the
template file, a conditional group will have the 'condition' attribute specified as the
name of a macro within the data file.

If the macro's value is equivalent to a false value, then none of the group's contents
are included in the resulting UI screen. Otherwise, the conditional is treated like a
basic group.

[Full Documentation](logic.md)


## Layouts

Layout nodes take a group of widgets and automatically position them, so that specific
x and y values don't need to be provided to each element. The layouts available to use
are Flows, Repeats, and the Grid.

* Flows arrange items along a given axis, placing each successive widget right after the
next one.

* Repeats will copy their children widgets as a group and repeat them along a given axis,
using a set of macros to configure each repeated line according to the user's input.

* Grids work like the Repeat node, but will copy the widgets according to
a grid pattern, using a specified ratio to determine the number of columns and rows.

[Full Documentation](layouts.md)


## Positioners

Positioners are a way to define a widget's position or size that is in some way dependent 
on the parent widget. There are two types of positioners provided, stretch and center.

* Stretches set the size of a widget's axis to the same value as the widget's parent.

* Centers set a widget's position so that the center of the widget aligns with the center
of its parent along a given axis.

[Full Documentation](positioners.md)
