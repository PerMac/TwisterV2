from __future__ import annotations

import logging

import pytest

from twister2.filter.tag_filter import TagFilter

logger = logging.getLogger(__name__)


class FilterPlugin:
    """Plugin for filtering tests."""

    def __init__(self, config: pytest.Config):
        self.config = config
        self.filters = [TagFilter(self.config)]

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(
        self, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
    ):
        selected_items = items
        deselected_items = []

        for filter_ in self.filters:
            selected_items, deselected_items = filter_.filter(selected_items)

        if deselected_items:
            config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items
