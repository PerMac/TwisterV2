from __future__ import annotations

from typing import Set, List, Sequence, Tuple

import pytest


class TagFilter:
    """Filter tests by tag."""

    def __init__(self, config: pytest.Config):
        self.config = config
        self.user_tags: list[str] = config.getoption('tags') or []

    def filter(self, items: list[pytest.Item]) -> Tuple[list[pytest.Item], list[pytest.Item]]:
        if self.user_tags:
            return self.get_selected_and_deselected_by_tags(items, self.user_tags)
        else:
            return items, []

    def get_selected_and_deselected_by_tags(
        self, items: list[pytest.Item], tags: Sequence[str]
    ) -> Tuple[list[pytest.Item], list[pytest.Item]]:
        selected_items = []
        deselected_items = []

        filters = TagMatcher(tags)

        for item in items:
            item_tags: set[str] = self.get_item_tags(item)

            if filters.should_run_with(item_tags):
                selected_items.append(item)
            else:
                deselected_items.append(item)
        return selected_items, deselected_items

    @staticmethod
    def get_item_tags(item: pytest.Item) -> Set[str]:
        """Return tags assigned to test item."""
        tags = []
        for marker in item.iter_markers(name='tags'):
            tags.extend(marker.args)
        return set(tags)


class TagMatcher:
    """Check if test item should be run or not."""

    def __init__(self, tags: Sequence[str] | None = None):
        self.selected: List[Set[str]] = []  #: store selected tags
        self.deselected: List[Set[str]] = []  #: store deselected tags
        if tags is None:
            tags = []
        self.parse(tags)

    def parse(self, item_tags: Sequence[str]) -> None:
        """
        :param item_tags: test tags separated by comma
        """
        for tags in item_tags:
            include_tags = set()
            exclude_tags = set()
            for tag in (t.replace('@', '') for t in tags.split(',')):
                if tag.startswith('~'):
                    exclude_tags.add(tag[1:])
                else:
                    include_tags.add(tag)
            if include_tags:
                self.selected.append(include_tags)
            if exclude_tags:
                self.deselected.append(exclude_tags)

    def should_run_with(self, tags: Set[str]) -> bool:
        results = []
        tags = set(tags)
        for selected_tags in self.selected:
            results.append(self._should_be_selected(tags, selected_tags))
        for deselected_tags in self.deselected:
            results.append(not self._should_be_deselected(tags, deselected_tags))
        return all(results)

    @staticmethod
    def _should_be_deselected(tags1: set, tags2: set) -> bool:
        return bool(tags1 & tags2)

    @staticmethod
    def _should_be_selected(tags1: set, tags2: set) -> bool:
        return bool(tags1 & tags2)
