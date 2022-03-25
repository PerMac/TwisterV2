"""
Module is responsible for searching and parsing yaml files, and generating test cases.

Base of non-python test definition:
https://github.com/pytest-dev/pytest/issues/3639
"""
import logging
from pathlib import Path
from typing import Generator

import pytest
import yaml

from twister2.config import TwisterConfig
from twister2.yaml_test_function import YamlTestFunction, yaml_test_function_factory
from twister2.yaml_test_specification import YamlTestSpecification

logger = logging.getLogger(__name__)


class YamlFile(pytest.File):
    """Class for collecting tests from a yaml file."""

    def collect(self):
        """Return a list of yaml tests."""
        twister_config = self.config.twister_config
        # read all tests from yaml file and generate pytest test functions
        for spec in _read_test_specifications_from_yaml(self.fspath, twister_config):
            test_function: YamlTestFunction = yaml_test_function_factory(spec=spec, parent=self)
            # extend xml report
            test_function.user_properties.append(('tags', ' '.join(spec.tags)))
            test_function.user_properties.append(('platform', spec.platform))
            yield test_function


def _generate_test_variants_for_platforms(
    spec: dict, twister_config: TwisterConfig
) -> Generator[YamlTestSpecification, None, None]:
    """Generate test variants according to provided platforms."""
    assert isinstance(twister_config, TwisterConfig)
    spec = spec.copy()
    selected_platforms = twister_config.platforms

    allowed_platform = spec.get('allowed_platform', '').split() or selected_platforms
    platform_exclude = spec.get('platform_exclude', '').split()
    test_name = spec['name']

    logger.debug('Generating tests for %s with selected platforms %s', test_name, selected_platforms)

    for platform in allowed_platform:
        if platform in platform_exclude:
            continue
        spec['name'] = test_name + f'[{platform}]'
        spec['platform'] = platform
        yaml_test_spec = YamlTestSpecification(**spec)
        logger.debug('Generated: %s', yaml_test_spec)
        yield yaml_test_spec


def _read_test_specifications_from_yaml(
    filepath: Path, twister_config: TwisterConfig
) -> Generator[YamlTestSpecification, None, None]:
    """
    Return generator of yaml test specifications.

    :param filepath: path to a yaml file
    :param twister_config: twister configuration
    :return: generator of yaml test specifications
    """
    yaml_tests: dict = yaml.safe_load(filepath.open())
    if yaml_tests.get('tests') is None:
        return

    sample = yaml_tests.get('sample', {})  # exists in yaml but it is not used
    common = yaml_tests.get('common', {})
    common['path'] = Path(filepath).parent

    for test_name, spec in yaml_tests['tests'].items():
        test_name: str
        spec: dict
        spec['name'] = test_name
        spec.update(common)

        for test_spec in _generate_test_variants_for_platforms(spec, twister_config):
            yield test_spec
