import logging

import pytest


def pytest_collection_modifyitems(session, config, items):
    selected_items = []
    deselected_items = []

    for item in items:
        selected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
    items[:] = selected_items


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item) -> None:
    logging.warning('setup')
