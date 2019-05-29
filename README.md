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

data = { 
    "key1": "foo",
    "key2": "bar"
}

if "data.json" not in z:
    z["data.json"] = data

assert data == z["data.json"]
```

## Options

Upon initialization various parameters can be given to customize the behaviour 
of the *ZipArchive* class. 

- **overwrite** (default: False): If a zipfile with the given filename exists, it will be truncated (i.e. overwritten)
- **json_ext** (default: ".json"): Files ending with json\_ext will be piped through json.loads upon retrieval
- **json_indent** (default: 4): The default indentation for json files is 4.

## Limitations

* You cannot remove/change file in the archive 

## License

MIT

## Copyright

Peter Mühleder and Universitätsbibliothek Leipzig, 2019
