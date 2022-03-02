"""
Non-python test definition.

https://github.com/pytest-dev/pytest/issues/3639
"""
import logging
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path

import pytest
import yaml
from _pytest.compat import NOTSET

logger = logging.getLogger(__name__)


@dataclass
class YamlTestSpecification:
    """Test specification for yaml test."""
    name: str
    path: Path  # path to a folder where C files are stored
    tags: str = ''
    filter: str = ''
    min_flash: str = ''
    build_only: bool = False
    harness: str = ''
    extra_configs: list[str] = field(default=list)
    integration_platforms: list = field(default=list)
    platform_allow: list = field(default=list)
    platform_exclude: list = field(default=list)


class YamlTestClass:
    """Test Function."""

    def __init__(self, name: str, spec: YamlTestSpecification):
        """
        :param name: test name
        :param spec: test specification     
        """
        self.name = name
        self.spec = spec
    
    def __call__(self):
        """Method called by pytest when it runs test."""
        logger.info('Test execution %s from %s', self.name, self.spec.path)
        logger.debug(self.spec)
        assert True


# TODO: Implement
class YamlFunction(pytest.Function):
    """Wraper for pytest.Function to extend functionality"""

    def __init__(
        self,
        name: str,
        spec,
        parent,
        config=None,
        callspec=None,
        callobj=NOTSET,
        keywords=None,
        session=None,
        fixtureinfo=None,
        originalname=None,
    ) -> None:
        super().__init__(name, parent, callspec, callobj, keywords, session, fixtureinfo, originalname)
        self.spec = spec


class YamlFile(pytest.File):
    """Class is used to load tests from yaml file."""

    def collect(self):
        """Read yaml file and extract tests from it."""
        yaml_tests = yaml.safe_load(self.fspath.open())
        if 'tests' not in yaml_tests:
            return None
        
        # read all tests from yaml file and generate pytest test functions
        for name, spec in sorted(yaml_tests['tests'].items()):
            spec_class = YamlTestSpecification(name, path=Path(self.fspath).parent, **spec)
            yield pytest.Function.from_parent(  # TODO: implement YamlFunction to replace it
                name=name,
                parent=self,
                callobj=YamlTestClass(name, spec_class),  # callable object (test function)
            )
