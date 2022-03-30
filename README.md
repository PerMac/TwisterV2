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
