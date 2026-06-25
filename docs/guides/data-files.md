---
layout: default
title: Using Data Files
parent: Guides
nav_order: 9
---

# Using Data Files
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

Gestalt layouts can accept external input data that gets substituted into the layout
as macros. Data is provided via the `--input` flag and can come in several formats.


## YAML

YAML is the most common input format. Provide a file with key-value pairs:

```yaml
# data.yml
MOTORS: 8
ASPECT: 2.0
PADDING: 15
PREFIX: "IOC1:"
```

```bash
python gestalt.py --to ui --input data.yml --output screen.ui layout.yml
```

Values are referenced in the layout with `{NAME}`:

```yaml
Grid: !Grid
    repeat-over: "MOTORS"
    aspect-ratio: "{ASPECT}"
    padding: "{PADDING}"
```

YAML data files can contain nested structures -- lists and dictionaries -- which are
useful for driving repeat nodes:

```yaml
CHANNELS:
    - { N: 1, label: "Channel 1", pv: "Ch1" }
    - { N: 2, label: "Channel 2", pv: "Ch2" }
```

Gestalt auto-detects YAML from `.yml` and `.yaml` file extensions. You can also
specify it explicitly with `--from yaml`.


## Inline YAML strings

For quick tests or simple data, you can pass a YAML string directly on the command
line instead of creating a file:

```bash
python gestalt.py --to ui --input "{MOTORS: 4, ASPECT: 2.0}" --from str --output screen.ui layout.yml
```

The `--from str` flag tells Gestalt to parse the `--input` value as a YAML string
rather than a file path.


## JSON

JSON files work the same way as YAML. Provide a JSON file with the macros:

```json
{
    "MOTORS": 8,
    "ASPECT": 2.0,
    "CHANNELS": [
        {"N": 1, "label": "Ch 1"},
        {"N": 2, "label": "Ch 2"}
    ]
}
```

```bash
python gestalt.py --to ui --input data.json --output screen.ui layout.yml
```

Auto-detected from `.json` file extension, or specify with `--from json`.


## EPICS substitutions

Gestalt can read EPICS substitution files (the format used by `msi` and `dbLoadTemplate`).
This is useful when your PV naming is already defined in a substitutions file:

```
file "motor.db"
{
    pattern { P, M, PORT }
    { "IOC1:", "m1", "serial1" }
    { "IOC1:", "m2", "serial1" }
    { "IOC1:", "m3", "serial2" }
}
```

```bash
python gestalt.py --to ui --input motors.substitutions --from msi --output screen.ui layout.yml
```

The parsed data is structured as a dictionary keyed by the database filename. Each
key maps to a list of dictionaries (one per substitution row). In the layout, you
would reference this as:

```yaml
Motors: !VRepeat
    repeat-over: "motor.db"
    padding: 5
    children:
        - !Apply:PVReadWrite
            label: "{M}:"
            read-pv: "{P}{M}.RBV"
```

Auto-detected from `.substitutions` file extension, or specify with `--from msi`.


## INI / config files

Python-style INI files are also supported:

```ini
[settings]
MOTORS = 8
ASPECT = 2.0
PADDING = 15
```

```bash
python gestalt.py --to ui --input config.cfg --output screen.ui layout.yml
```

Values are accessed as `{section[key]}` using Python's format string dictionary
access syntax:

```yaml
Grid: !Grid
    repeat-over: "{settings[MOTORS]}"
    aspect-ratio: "{settings[ASPECT]}"
```

Auto-detected from `.ini` and `.cfg` file extensions, or specify with `--from ini`.


## Format auto-detection

When you use `--input` without `--from`, Gestalt infers the format from the file
extension:

| Extension | Format |
|-----------|--------|
| `.yml`, `.yaml` | YAML |
| `.json` | JSON |
| `.substitutions` | EPICS substitutions |
| `.ini`, `.cfg` | INI config |

If the extension is not recognized, use `--from` to specify the format explicitly.

---

## Next steps

- [Command Line Options](../reference/commandline) -- Full command-line option reference.
- [Repeat and Grid](repeat-and-grid) -- How to use repeated data in layouts.
- [Macro Resolution](../concepts/macros) -- How macros are substituted in property values.
