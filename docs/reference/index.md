---
layout: default
title: Reference
nav_order: 5
has_children: true
---

## Nodes

The default element underlying the generation of any output files in Gestalt is
the Node. A template file is just a set of Nodes that, when provided with user 
input data, will write out all the UI widgets for a given generated screen.

Nodes can represent individual UI widgets, repetitions of UI widgets within a layout,
certain computational logic, or offset positioning.

[Full Documentation](nodes/index.md)


## Built-in Widget Templates

Using the Template/Apply nodes, the same set of nodes can be copied multiple times
throughout a gestalt template file. Gestalt comes included with a collection of preset 
templates that provide reusable sets of associated nodes for the purpose of standardizing
semi-complex tasks. 

For example, the OnOffText template provides two colored labels that will turn on and off
visibility based off of a provided PV. A setup that is frequently used to display a
connection status or an idle/active state.

[Full Documentation](templates/index.md)
