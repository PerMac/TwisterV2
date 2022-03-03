"""
Non-python test definition.

https://github.com/pytest-dev/pytest/issues/3639
"""
import logging
from functools import partial
from pathlib import Path

import pytest
import yaml
from _pytest.compat import NOTSET

from .yaml_test_class import YamlFunction, YamlTestClass, YamlTestSpecification

logger = logging.getLogger(__name__)


def read_test_specifications_from_yaml(filepath: Path) -> list[YamlTestSpecification]:
    """
    Return list of specification for tests.

    :param filepath: path to a yaml file
    :return: list of yaml test specification
    """
    yaml_tests: dict = yaml.safe_load(filepath.open())
    if not yaml_tests.get('tests'):
        return []

    tests_list: list[YamlTestSpecification] = []
    sample = yaml_tests.get('sample', {})
    common = yaml_tests.get('common', {})
    common['path'] = Path(filepath).parent

    for test_name, spec in yaml_tests['tests'].items():
        test_name: str
        spec: dict
        spec['name'] = test_name
        spec.update(common)
        tests_list.append(YamlTestSpecification(**spec))

    return tests_list


class YamlFile(pytest.File):
    """Class for collecting tests from a yaml file."""

    def collect(self):
        """Return a list of yaml tests."""
        # read all tests from yaml file and generate pytest test functions
        for spec in read_test_specifications_from_yaml(self.fspath):
            test_function: YamlFunction = YamlFunction.from_parent(
                name=spec.name,
                parent=self,
                callobj=YamlTestClass(spec),  # callable object (test function)
            )
            # logger.info(dir(test_function))
            test_function.add_marker('debug')
            logger.info(test_function.parent)
            yield test_function
