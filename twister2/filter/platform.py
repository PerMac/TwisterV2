"""
Filter implementation to filter twister tests by platform.
"""
from __future__ import annotations

import pytest
from twister2.config import TwisterConfig
from twister2.helper import is_yaml_test


class PlatformFilter:
    """Filter tests by platform"""

    def __init__(self, twister_config: TwisterConfig) -> None:
        """
        :param twister_config: twister configuration
        """
        #: list of platforms selected from commandline 
        self.selected_platforms: set[str] = set(twister_config.platform)

    def filter(self, items: list[pytest.Item]) -> tuple[list[pytest.Item], list[pytest.Item]]:
        """
        Filter list of items and return two list with selected and deselected items.
        
        :param items: list of pytest items
        :return: tuple with selected and deselected items
        """
        selected_items = []
        deselected_items = []

        for item in items:
            if is_yaml_test(item):
                if self._should_run(item):
                    selected_items.append(item)
                else:
                    deselected_items.append(item)
            else:
                selected_items.append(item)  # we don't filter other tests
        return selected_items, deselected_items

    def _should_run(self, item: pytest.Item) -> bool:
        """Return if item should be select to execution."""
        platform_allow: set[str] = set(item.function.spec.platform_allow)
        if platform_allow & self.selected_platforms:
            return True
        else:
            return False
