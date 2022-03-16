# twister v2

Run tests:
```
pytest tests
```

Show test plan:
```
pytest tests --setup-plan
```

List all tests without executing
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
