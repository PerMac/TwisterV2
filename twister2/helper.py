import logging

import pytest

from twister2.yaml_test_function import YamlTestFunction


def is_yaml_test(item: pytest.Item) -> bool:
    """Return True if item is a yaml test."""
    if isinstance(item, YamlTestFunction):
        return True
    else:
        return False


def configure_logging(config: pytest.Config) -> None:
    log_level = config.getoption('--log-level') or logging.INFO
    log_file = config.getoption('--log-file') or 'twister2.log'
    logging.basicConfig(
        level=log_level,
        filename=log_file,
        filemode='w',
        format='%(levelname)-8s:%(name)s: %(message)s'
    )
