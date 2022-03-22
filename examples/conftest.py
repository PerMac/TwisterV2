from __future__ import annotations

import logging
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parents[1]))


logging.basicConfig(
    level=logging.DEBUG,
    filename='test.log',
    filemode='w',
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
        if hasattr(item.function, 'spec'):
            logger.debug(item.function.spec)
        selected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
    items[:] = selected_items


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    logger.info('setup item %s', repr(item))
