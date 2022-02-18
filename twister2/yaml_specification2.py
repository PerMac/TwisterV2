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

logger = logging.getLogger(__name__)


def pytest_collect_file(parent, path):
    if path.ext == ".yaml":
        return YamlFile.from_parent(parent, path=Path(path))


@dataclass
class YamlTestSpecification:
    name: str
    min_flash: str
    tags: str = ''
    filter: str = ''
    extra_configs: list[str] = field(default=list)


class YamlTestClass:
    """Test Function."""

    def __init__(self, name, spec):
        self.name = name
        self.spec = spec

    def __call__(self, my_awesome_fixture):
        logger.info('Test execution %s', self.name)
        assert True


def my_custom_test_function(spec, my_awesome_fixture):
    """Test funcition"""
    logger.info(spec)
    assert True


@pytest.fixture
def my_awesome_fixture():
    logger.info('awsome fixture')


class YamlFile(pytest.File):

    def collect(self):
        yaml_tests = yaml.safe_load(self.fspath.open())
        if 'tests' not in yaml_tests:
            return None
        for name, spec in sorted(yaml_tests['tests'].items()):
            spec_class = YamlTestSpecification(name, **spec)
            if spec_class.tags:
                pass

            # callobj = partial(my_custom_test_function,spec)
            callobj = partial(YamlTestClass(name, spec_class))

            yield pytest.Function.from_parent(
                parent=self,
                name=name,
                callobj=callobj,
            )
