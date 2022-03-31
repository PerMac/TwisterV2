# twister v2

## Installation

Installation from the source:
```
pip install .
```

Build wheel package:
```
pip install build
python -m build --wheel
```

## Requirements:

- Python >= 3.8
- pytest >= 7.0.0

## Usage

Show all available options:
```
pytest --help
```

Run tests:
```
pytest tests --zephyr-base=path_to_zephyr
```

Show test plan:
```
pytest tests --setup-plan
```

List all tests without executing:
```
pytest tests --collect-only
```

Generate test plan in CSV format:
```
pytest tests --testplan-csv=testplan.csv --collect-only
```

Generate test results in JSON format:
```
pytest tests --resutls-json=results.json
```

Generate tests for specific platforms:
```
pytest tests --platform=qemu_x86 --platform=nrf51dk_nrf51422
```

Generate JUnit report with results:
```
pytest tests --junitxml=results.xml
```

## Filtering tests

Run tests with given tags (`@` is optional and can be omitted):
```
$ pytest tests --tags=@tag1,@tag2
```

Examples of usage:

* not tag1
  * --tags=~@tag1
* tag1 and tag2:
  * --tags=@tag1 --tags=@tag2
* tag1 or tag2
  * --tags=@tag1,@tag2
* (tag1 or tag2) and tag3 and not tag4
  * --tags=@tag1,@tag2 --tags=@tag3 --tags=~@tag4


## Available options

```
Twister reports:
  --testplan-csv=PATH   generate test plan in CSV format
  --testplan-json=PATH  generate test plan in JSON format
  --results-json=PATH   generate test results report in JSON format

Twister:
  --build-only          build only
  --platform=PLATFORM   build tests for specific platforms
  --board-root=PATH     directory to search for board configuration files
  --zephyr-base=path    base directory for Zephyr
  --tags=TAGS           filter test by tags, e.g.: --tags=@tag1,~@tag2 --tags=@tag3
```
