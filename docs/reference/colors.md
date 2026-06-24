---
layout: default
title: Colors
parent: Reference
nav_order: 4
---

# Color Reference
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

The `colors.yml` include file defines named colors as YAML anchors. Include it in your
layout and reference colors with the `*` dereference character:

```yaml
#include colors.yml

Label: !Text
    foreground: *white
    background: *header_blue
```


## CSS named colors

The primary collection of colors in `colors.yml` consists of the
[standard 140 CSS/HTML named colors](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color).
These are available using their standard lowercase names:

```yaml
foreground: *red
background: *lightskyblue
border-color: *darkslategray
```

All 140 standard CSS color names are defined (e.g., `*aliceblue`, `*coral`,
`*darkgoldenrod`, `*forestgreen`, `*lightsalmon`, `*mediumseagreen`, `*papayawhip`,
`*steelblue`, `*yellowgreen`, etc.).


## Gestalt-specific colors

In addition to the CSS colors, `colors.yml` defines several colors that are commonly
used in EPICS control screens but are not part of the CSS standard:

### Special

| Anchor | Value | Description |
|--------|-------|-------------|
| `*transparent` | `$00000000` | Fully transparent (alpha = 0) |

### Alarm colors

| Anchor | Value | Description |
|--------|-------|-------------|
| `*alarm_red` | `$E41E1E` | Standard alarm red |
| `*alarm_yellow` | `$E4E41E` | Standard alarm yellow |
| `*alarm_green` | `$1EE41E` | Standard alarm green |

### Blacks and whites

| Anchor | Value | Description |
|--------|-------|-------------|
| `*pure_black` | `$000000` | True black |
| `*black` | `$242424` | Slightly softened black (default text color) |
| `*pure_white` | `$FFFFFF` | True white |
| `*white` | `$E4E4E4` | Slightly softened white |

### Greys

Both `grey` and `gray` spellings are defined for each shade:

| Anchor | Value |
|--------|-------|
| `*grey_darker` / `*gray_darker` | `$444444` |
| `*grey_dark` / `*gray_dark` | `$646464` |
| `*grey` / `*gray` | `$848484` |
| `*grey_light` / `*gray_light` | `$A4A4A4` |
| `*grey_lighter` / `*gray_lighter` | `$C4C4C4` |

### UI colors

| Anchor | Value | Description |
|--------|-------|-------------|
| `*edit_blue` | `$57CAE4` | Background for editable fields |
| `*menu_green` | `$358400` | Menu/choice selected color |
| `*link_pink` | `$D494E4` | EPICS record dynamic link fields |
| `*link_purple` | `$9494E4` | Alternate dynamic link field color |
| `*header_blue` | `$003584` | Screen header background |


## Color schemes

The `color-schemes.yml` file (included by `widgets.yml`) defines preset attribute
bundles that can be applied to widgets with the YAML merge operator `<<`:

| Anchor | Properties |
|--------|------------|
| `*editable` | foreground: `*black`, background: `*edit_blue` |
| `*string_display` | foreground: `*black`, background: `*transparent` |
| `*data_display` | foreground: `*alarm_green`, background: `*gray_darker`, alignment: Center |
| `*centered_label` | foreground: `*black`, background: `*transparent`, alignment: Center |
| `*alarm_led` | false-color: `*alarm_green`, true-color: `*alarm_red` |
| `*colored_label` | foreground: `*header_blue`, background: `*transparent` |

Usage:

```yaml
#include color-schemes.yml

Readback: !TextMonitor
    <<: *data_display
    geometry: 100x20
    pv: "$(P)Value"
```
