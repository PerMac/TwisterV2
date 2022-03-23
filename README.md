# twister v2

Requirements:

- Python >= 3.8
- pytest >= 7.0.0

Run tests:
```
pytest tests
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
pytest tests --testplan=testplan.csv --collect-only
```

Filter tests by platform:
```
pytest tests --platform="qemu_x86,nrf51dk_nrf51422"
```

Generate JUnit report with results:
```
pytest tests --junitxml=results.xml
```
