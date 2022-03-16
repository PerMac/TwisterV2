from __future__ import annotations
from distutils.command.config import config

import logging
from typing import Protocol

import pytest
from twister2.config import TwisterConfig
from twister2.filter.platform import PlatformFilter

logger = logging.getLogger(__name__)


class FilterInterface(Protocol):
    def __init__(self, twister_config: TwisterConfig): ...
    def filter(item: list[pytest.Item]) -> tuple[list[pytest.Item], list[pytest.Item]]: ...


class FilterPlugging:
    """Plugin for filtering tests"""

    def __init__(self, config: pytest.Config) -> None:
        self.config = config

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(
        self, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
    ):
        logger.debug('Filering tests')
        twister_config = config.twister_config

        selected_items, deselected_items = PlatformFilter(twister_config).filter(items)

        if deselected_items:
            config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items
