---
layout: default
title: embedded-motor.yml
parent: Templates
nav_order: 1
---

# embedded-motor.yml
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


### EmbeddedMotor

A 160x210 mini motor control area. 


* **Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| motor-pv     | String | The full pv for the motor to be controlled |


* **Example**

```yaml
motor_grid: !grid
    variable: "N"
    start-at: 1
    repeat-over: 10
    
    children:
        - !Apply:EmbeddedMotor
            motor-pv: "$(P)$(M{N})"
```
