"""
Plugin to generate test plan report
"""
from __future__ import annotations

import logging
import os
from typing import List, Protocol, Union

import pytest
from _pytest.terminal import TerminalReporter
from twister2.report.helper import (get_item_platform_allow, get_item_tags,
                                    get_item_type, get_test_name)

logger = logging.getLogger(__name__)


class SpecReportInterface(Protocol):
    def __init__(self, filename: str) -> None: ...
    def write(self, data: list[dict]) -> None: ...


# FIXME: does not work with pytest-xdist, needs some refactoring
class TestPlanPlugin:
    """
    Generate TestPlan as CSV.

    :param logfile: output filename
    :param config: pytest.Config
    :param writers:
    """

    def __init__(
        self,
        config: pytest.Config,
        writers: Union[SpecReportInterface, list[SpecReportInterface]]
    ):
        self.config = config
        if not isinstance(writers, list):
            writers = [writers]
        self.writers = writers

    def _item_as_dict(self, item: pytest.Item) -> dict:

        return dict(
            suite_name=item.nodeid,
            test_name=get_test_name(item),
            tags=get_item_tags(item),
            type=get_item_type(item),
            platform_allow=get_item_platform_allow(item),
        )

    def generate(self, items: List[pytest.Item]) -> list[dict]:
        """Build test plan and save."""
        return [self._item_as_dict(item) for item in items]

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]):
        if config.getoption('testplan_path'):
            data = self.generate(items)
            self._save_report(data)

    def pytest_terminal_summary(self, terminalreporter: TerminalReporter) -> None:
        # print summary to terminal
        terminalreporter.ensure_newline()
        for writer in self.writers:
            terminalreporter.write_sep('-', f'generated testplan file: {writer.filename}', green=True)

    def _save_report(self, report_content: List[dict]) -> None:
        for writer in self.writers:
            writer.write(report_content)
