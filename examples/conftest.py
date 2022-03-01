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
pytest_plugins = (
    'twister2.plugin',
)


logger = logging.getLogger(__name__)


def pytest_collection_modifyitems(session: pytest.Session, config: pytest.Config, items: list[pytest.Item]):
    logger.info('Modyfing tests before run')
    selected_items = []
    deselected_items = []

    for item in items:
        selected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
    items[:] = selected_items


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    logger.info('setup item %s', repr(item))
