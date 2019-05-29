# ZipArchive

ZipArchive class for easy/quick data storage (text and json files).

## Installation

1. Clone repo

```zsh

$ git clone https://github.com/missinglinks/zip_archive.git

```

2. Install with pip

```zsh

$ cd zip_archive
$ pip install .

```

## Usage

```python

from zip_archive import ZipArchive

z = ZipArchive("test.zip")

y = { "a": "bc" }

if not z.contains("y.json"):
    z.add("y.json", y)

y = z.get("y.json")

```

## Limitations

* You cannot remove/change file in the archive 