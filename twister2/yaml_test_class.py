"""
Yaml test implementation.

https://docs.pytest.org/en/6.2.x/example/nonpython.html
"""
from __future__ import annotations

import logging
from typing import Any

import pytest

from twister2.log_parser import LogParser
from twister2.yaml_test_specification import YamlTestSpecification

logger = logging.getLogger(__name__)


def yaml_test_function_factory(spec: YamlTestSpecification, parent: Any) -> YamlTestFunction:
    """Generate test function."""
    return YamlTestFunction.from_parent(
        name=spec.name,
        parent=parent,
        callobj=YamlTestClass(spec),  # callable object (test function)
    )


class YamlTestFunction(pytest.Function):
    """Wrapper for pytest.Function to extend functionality"""

    def setup(self) -> None:
        """Setup test function."""
        logger.debug('Setup test %s', repr(self))
        logger.debug('Callobj = %s', self.obj)
        return super().setup()

    def teardown(self) -> None:
        """Teardown test function."""
        logger.debug('Teardown test %s', repr(self))
        return super().teardown()


class YamlTestClass:
    """Callable class representing test."""

    def __init__(self, spec: YamlTestSpecification, description: str = ''):
        """
        :param spec: test specification
        :param description: test description (docstring)
        """
        self.spec = spec
        self.__doc__ = description

    def __call__(self, subtests, log_parser: LogParser, builder, *args, **kwargs):
        """Method called by pytest when it runs test."""
        logger.info('Execution test %s from %s', self.spec.name, self.spec.path)

        if log_parser is None:
            return

        # using subtests fixture to log single C test
        # https://pypi.org/project/pytest-subtests/
        for i, test in enumerate(log_parser.parse()):
            logger.debug('Subtest status: %s', test)

            with subtests.test(msg=test.testname, i=i):
                assert test.result == 'PASS', f'Subtest {test.testname} failed'
