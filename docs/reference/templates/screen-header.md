---
layout: default
title: screen-header.yml
parent: Templates
nav_order: 4
---

# screen-header.yml
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


### ScreenHeader

A simple header banner for screens. Uses a horizontal stretch to reach across the entire, generated screen.
Because of this, slightly counterintuitively, this should be included as the last element of the screen,
with all other elements having their geometries set up to start after the height value used.

* **Attributes**

|     Name         |  Type     | Description|
|------------------|-----------|------------|
| height           | Number    | The height of the resulting header, default: 45 |
| title            | String    | Text to display in the header |
| alignment        | Alignment | Text alignment for the header, default: Center |
| fontname         | String    | Name of font for display text, default: "Liberation Sans" |
| background-color | Color     | Header background color, default: *header_blue |
| text-color       | Color     | Header text color, default: *white |

* **Example**

```yaml
UITitle: !Apply:ScreenHeader { title: "$(P)$(SLITS)" }
```
