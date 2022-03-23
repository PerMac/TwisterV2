"""
Plugin to generate test plan report
"""
from __future__ import annotations

import logging
from typing import List, Protocol, Union

import pytest
from _pytest.terminal import TerminalReporter
from twister2.report.helper import (
    get_item_platform_allow,
    get_item_tags,
    get_item_type,
    get_test_name,
)

logger = logging.getLogger(__name__)


class SpecReportInterface(Protocol):
    def write(self, data: list[dict]) -> None: ...


# FIXME: does not work with pytest-xdist, needs some refactoring
class TestPlanPlugin:
    """Generate TestPlan as CSV."""

    def __init__(
        self,
        config: pytest.Config,
        writers: Union[SpecReportInterface, list[SpecReportInterface]]
    ):
        """
        :param config: pytest.Config
        :param writers: list of SpecReportInterface
        """
        self.config = config
        if not isinstance(writers, list):
            writers = [writers]
        self.writers = writers

    def _item_as_dict(self, item: pytest.Item) -> dict:
        """Return test metadata as dictionary."""
        return dict(
            suite_name=item.nodeid,
            test_name=get_test_name(item),
            tags=get_item_tags(item),
            type=get_item_type(item),
            platform_allow=get_item_platform_allow(item),
        )

    def generate(self, items: List[pytest.Item]) -> list[dict]:
        """Build test plan"""
        return [self._item_as_dict(item) for item in items]

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]):
        # generate test plan and save
        if config.getoption('testplan_path'):
            data = self.generate(items)
            self._save_report(data)

    def pytest_terminal_summary(self, terminalreporter: TerminalReporter) -> None:
        # print summary to terminal
        terminalreporter.ensure_newline()
        for writer in self.writers:
            terminalreporter.write_sep('-', f'generated testplan file: {writer.filename}', green=True)

    def _save_report(self, data: List[dict]) -> None:
        for writer in self.writers:
            writer.write(data)
