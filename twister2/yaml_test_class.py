"""
Yaml test implementation.

https://docs.pytest.org/en/6.2.x/example/nonpython.html
"""
from __future__ import annotations

import logging

import pytest

from twister2.yaml_test_specification import YamlTestSpecification

logger = logging.getLogger(__name__)


def yaml_test_function_factory(spec, parent) -> YamlFunction:
    """Generate test function."""
    return YamlFunction.from_parent(
        name=spec.name,
        parent=parent,
        callobj=YamlTestClass(spec),  # callable object (test function)
    )


class YamlFunction(pytest.Function):
    """Wraper for pytest.Function to extend functionality"""

    # def __init__(
    #     self,
    #     name: str,
    #     spec,
    #     parent,
    #     config=None,
    #     callspec=None,
    #     callobj=NOTSET,
    #     keywords=None,
    #     session=None,
    #     fixtureinfo=None,
    #     originalname=None,
    # ) -> None:
    #     super().__init__(name, parent, callspec, callobj, keywords, session, fixtureinfo, originalname)
    #     self.spec = spec

    def setup(self) -> None:
        logger.debug('Setup test %s', repr(self))
        logger.debug('Callobj = %s', self.obj)
        return super().setup()

    def teardown(self) -> None:
        logger.debug('Teardown test %s', repr(self))
        return super().teardown()


class YamlTestClass:
    """Test Function."""

    def __init__(self, spec: YamlTestSpecification, description: str = ''):
        """
        :param name: test name
        :param spec: test specification
        :param description: test description (docstring)
        """
        self.spec = spec
        self.__doc__ = description

    def __call__(self, subtests, *args, **kwargs):
        """Method called by pytest when it runs test."""
        logger.info('Test execution %s from %s', self.spec.name, self.spec.path)
        logger.debug(self.spec)
        # https://pypi.org/project/pytest-subtests/
        # from .log_parser import LogParser
        # sub_tests = LogParser(open(r'zephyr_logs/threads_lifecycle.log')).parse_logs()
        # for i, test in enumerate(sub_tests):
        #     with subtests.test(msg=test.testname, i=i):
        #         assert test.result != 'PASS'

        # assert True
