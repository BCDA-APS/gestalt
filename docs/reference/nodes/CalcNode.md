---
layout: default
title: CalcNode
parent: Nodes
nav_order: 5
has_toc: false
---


# CalcNode

An invisible widget which can perform a calculation on a set of input PVs and provides the output as a PV local to the screen.

Since different UI tools use different syntax to configure their equivalent calc tools, the calculation attribute here should
be written as a general python statement. The supported operators are bitwise, negation, comparators, basic math, exponents,
and boolean operations.


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| pv         | String | The name used to reference the output values |
| A          | String | Input PV, the value of which can be referenced as A in the calculation |
| B          | String | Input PV, the value of which can be referenced as B in the calculation |
| C          | String | Input PV, the value of which can be referenced as C in the calculation |
| D          | String | Input PV, the value of which can be referenced as D in the calculation |
| calc       | String | The calculation to perform, provided in python syntax |


* **Example**

```yaml

# If the motor reports having GAIN_SUPPORT, show enable/disable LED
EnableCalc: !Calc
        A:    "{motor-pv}.MSTA"
        calc: "(A&2048)==2048"
        pv:   "{motor-pv}:TorqueDisplay"
        
EnableLED: !VStretch:Group
        visibility: "{motor-pv}:TorqueDisplay"
        children:
                - !VCenter:Group
                        children:
                                - !Apply:OnOffLED
                                        size: "{on-off-width}"
                                        control-pv: "{motor-pv}.CNEN"

```