import enum
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml


class ResultStatus(enum.Enum):
    NOTRUN = 'NOTRUN'
    PASSED = 'PASSED'
    FAILED = 'FAILED'
    SKIPPED = 'SKIPPED'


@dataclass
class Result:
    """Store result for ran test"""
    status: ResultStatus = ResultStatus.NOTRUN
    message: str = ""


class TwisterSpec:
    """Store test specification for C tests"""

    def __init__(self, name, spec):
        self.name = name
        self.spec = spec
        self.result = Result()

    def run_test(self) -> bool:
        self.result.status == ResultStatus.PASSED
        return True

    def assert_result(self):
        assert self.result.status == ResultStatus.PASSED


def load_tests(path: str) -> list[dict]:
    """Load test specifications from yaml file"""
    raw = yaml.safe_load(Path(path).open())
    return (TwisterSpec(name, spec)for name, spec in sorted(raw.items()))


def load_c_test(path: str):
    """
    Decorator for test function

    param path: path to yaml file with tests specification
    """
    tests = load_tests(path)

    def idfn(val):
        if isinstance(val, TwisterSpec):
            return val.name

    def decorator(func):
        return pytest.mark.parametrize(
            'spec', tests, ids=idfn
        )(func)

    return decorator
