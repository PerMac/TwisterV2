"""Load tests from yaml file."""
import enum
import logging
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

logger = logging.getLogger(__name__)


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
        logger.info('Run test %s', repr(self))
        for name, value in sorted(self.spec.items()):
            # Some custom test execution (dumb example follows).
            if name != value:
                self.result = Result(
                    ResultStatus.FAILED,
                    f"Expected: {value},\nbut was: {name}"
                )
                return False
        self.result = Result(ResultStatus.PASSED)
        return True

    def assert_result(self):
        assert self.result.status == ResultStatus.PASSED, self.result.message


def load_tests(path: str) -> list[dict]:
    """Load test specifications from yaml file"""
    raw = yaml.safe_load(Path(path).open())
    return (TwisterSpec(name, spec) for name, spec in sorted(raw.items()))


def load_c_test(path: str, *, ids=None):
    """
    Load test specification for yaml file.

    :param path: path to yaml file with tests specification
    :param ids:
    """
    tests = load_tests(path)

    def idfn(val):
        if isinstance(val, TwisterSpec):
            return val.name
    if ids is None:
        ids = idfn

    def decorator(func):
        return pytest.mark.parametrize(
            'spec', tests, ids=ids
        )(func)

    return decorator
