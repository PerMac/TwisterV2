"""
Yaml test implementation.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from _pytest.compat import NOTSET

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class YamlTestSpecification:
    """Test specification for yaml test."""
    name: str  #: test case name
    path: Path  #: path to a folder where C files are stored
    tags: set = field(default=set)
    type: str = 'integration'
    filter: str = ''
    min_flash: int = 32
    arch_allow: set = field(default=set)
    arch_exclude: set = field(default=set)
    build_only: bool = False
    build_on_all: bool = False
    skip: bool = False
    slow: bool = False
    timeout: int = 60
    min_ram: int = 8
    depends_on: set = field(default=set)
    harness: str = ''
    extra_sections: list = field(default=list)
    extra_configs: list[str] = field(default=list)
    extra_args: list[str] = field(default=list)
    integration_platforms: list = field(default=list)
    platform_allow: set = field(default=set)
    platform_exclude: set = field(default=set)
    harness_config: dict = field(default=dict)
    toolchain_exclude: set = field(default=set)
    toolchain_allow: set = field(default=set)

    def __post_init__(self):
        if isinstance(self.tags, str):
            self.tags = self.tags.split(' ')


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
        # self.name = name
        self.spec = spec
        self.__doc__ = description

    def __call__(self):
        """Method called by pytest when it runs test."""
        logger.info('Test execution %s from %s', self.spec.name, self.spec.path)
        logger.debug(self.spec)
        assert True

    @pytest.hookimpl(tryfirst=True)
    def pytest_generate_tests(self, metafunc):
        logger.debug('metafunc = %s', metafunc)
