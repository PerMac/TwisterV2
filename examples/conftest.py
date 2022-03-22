from __future__ import annotations

import logging
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parents[1]))

from twister2.helper import is_yaml_test

logging.basicConfig(
    level=logging.DEBUG,
    filename='test.log',
    filemode='w',
    format='%(levelname)-8s:%(name)s: %(message)s'
)

# list of plugins which should be loaded by pytest
# no need to use if plugin is installed (pip install ...)
# we can consider make a twister v2 python package
pytest_plugins = (
    'twister2.plugin',
)


logger = logging.getLogger(__name__)


def pytest_collection_modifyitems(
    session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
):
    logger.info('Modyfing tests before run')
    selected_items = []
    deselected_items = []

    for item in items:
        # example how to access test function
        if is_yaml_test(item):
            selected_items.append(item)
        else:
            deselected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
    items[:] = selected_items


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    logger.info('Setup item %s', repr(item))


def pytest_generate_tests(metafunc):
    # does not work with yaml tests!
    logger.debug('metafunc = %s', metafunc.function.__name__)
