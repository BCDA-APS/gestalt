---
layout: default
title: digital-io.yml
parent: Templates
grand_parent: Reference
nav_order: 6
---

# digital-io.yml
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


### HDigitalBit

A single digital I/O bit displayed as a vertical column. Intended for use inside an `!HRepeat`
where each bit is a column arranged horizontally.

Contains: a label, an input LED, an optional output choice button, an optional direction choice
button, and a description entry field, stacked vertically.

* **Attributes**

|     Name        |  Type  | Description|
|-----------------|--------|------------|
| prefix          | String | PV prefix, default: "$(P)" |
| bit-label       | String | Display label for this bit, default: "{N}" |
| input-pv        | String | PV for the input LED, default: "{prefix}Bi{N}" |
| output-pv       | String | PV for the output choice button, default: "{prefix}Bo{N}" |
| direction-pv    | String | PV for the direction choice button, default: "{prefix}Bd{N}" |
| desc-pv         | String | PV for the description entry, default: "{prefix}Bi{N}.DESC" |
| show-output     | Bool   | Whether to show the output choice button, default: true |
| show-direction  | Bool   | Whether to show the direction choice button, default: true |
| bit-width       | Number | Width of each bit column, default: 50 |
| height          | Number | Height of the label and LED, default: 20 |


* **Example**

```yaml
- !HRepeat
    repeat-over: 8
    padding: 5
    children:
        - !Apply:HDigitalBit
            prefix: "$(P)"
```


### VDigitalBit

A single digital I/O bit displayed as a horizontal row. Intended for use inside a `!VRepeat`
where each bit is a row arranged vertically.

Contains: a label, an input LED, an optional output choice button, an optional direction choice
button, and a description entry field, arranged horizontally.

* **Attributes**

|     Name        |  Type  | Description|
|-----------------|--------|------------|
| prefix          | String | PV prefix, default: "$(P)" |
| bit-label       | String | Display label for this bit, default: "{N}" |
| input-pv        | String | PV for the input LED, default: "{prefix}Bi{N}" |
| output-pv       | String | PV for the output choice button, default: "{prefix}Bo{N}" |
| direction-pv    | String | PV for the direction choice button, default: "{prefix}Bd{N}" |
| desc-pv         | String | PV for the description entry, default: "{prefix}Bi{N}.DESC" |
| show-output     | Bool   | Whether to show the output choice button, default: true |
| show-direction  | Bool   | Whether to show the direction choice button, default: true |
| label-width     | Number | Width of the bit label, default: 30 |
| led-width       | Number | Width of the LED indicator, default: 25 |
| choice-width    | Number | Width of each choice button, default: 80 |
| desc-width      | Number | Width of the description entry, default: 120 |
| height          | Number | Height of the row, default: 20 |
| spacing         | Number | Horizontal spacing between elements, default: 5 |


* **Example**

```yaml
- !VRepeat
    repeat-over: 8
    padding: 5
    children:
        - !Apply:VDigitalBit
            prefix: "$(P)"
            show-direction: false
```


### DigitalBitList

A complete list of digital I/O bits, repeated either horizontally (as vertical columns) or
vertically (as horizontal rows). Uses `HDigitalBit` or `VDigitalBit` internally based on
the `horizontal` attribute.

The `bits` attribute accepts either a number (for a contiguous range starting at `start-at`)
or a list of specific bit numbers.

* **Attributes**

|     Name        |  Type       | Description|
|-----------------|-------------|------------|
| bits            | Number/List | Number of bits to display, or a list of specific bit numbers, default: 8 |
| start-at        | Number      | Starting bit number when `bits` is a number, default: 0 |
| horizontal      | Bool        | true = vertical columns repeated horizontally, false = horizontal rows repeated vertically, default: true |
| show-output     | Bool        | Whether to show output choice buttons, default: true |
| show-direction  | Bool        | Whether to show direction choice buttons, default: true |
| padding         | Number      | Spacing between bits, default: 5 |

Any additional attributes (such as `prefix`, `input-pv`, `output-pv`, `direction-pv`, `desc-pv`)
are passed through to the inner bit templates via the macro environment. This allows overriding
the default PV naming convention without explicitly passing each parameter.


* **Examples**

Basic usage with 8 bits:

```yaml
- !Apply:DigitalBitList
    prefix: "$(P)"
    bits: 8
```

Vertical rows with no direction control:

```yaml
- !Apply:DigitalBitList
    prefix: "$(P)"
    bits: 16
    horizontal: false
    show-direction: false
```

Custom PV naming — overrides flow through to inner bit templates:

```yaml
- !Apply:DigitalBitList
    prefix: "$(P)myDevice:"
    bits: 4
    input-pv: "{prefix}DI{N}"
    output-pv: "{prefix}DO{N}"
    desc-pv: "{prefix}DI{N}.DESC"
    show-direction: false
```

Specific bit numbers from a list:

```yaml
- !Apply:DigitalBitList
    prefix: "$(P)"
    bits: [0, 2, 4, 6]
    show-output: false
```

Per-bit PV overrides using the bit template directly with a list of dicts:

```yaml
- !VRepeat
    padding: 5
    repeat-over:
        - { N: 0, desc-pv: "$(P)customDesc0" }
        - { N: 1, desc-pv: "$(P)customDesc1" }
        - { N: 2 }
        - { N: 3 }
    children:
        - !Apply:VDigitalBit
            prefix: "$(P)"
            show-direction: false
```
