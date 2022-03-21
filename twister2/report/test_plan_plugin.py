"""
Plugin to generate test plan report
"""
from __future__ import annotations

import logging
import os
from typing import List, Protocol

import pytest
from _pytest.terminal import TerminalReporter
from twister2.report.test_plan_csv import CsvTestPlan
from twister2.yaml_test_class import YamlFunction

logger = logging.getLogger(__name__)


class SpecReportInterface(Protocol):
    def __init__(self, filename: str) -> None: ...
    def write(self, data: list[dict]) -> None: ...


# FIXME: does not work with pytest-xdist, needs some refactoring
class TestPlanPlugin:
    """
    Generate TestPlan as CSV.

    :param logfile: output filename
    :param config: pytest._Config
    """

    def __init__(
        self,
        logfile: str,
        config: pytest.Config,
        writer: SpecReportInterface
    ):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.normpath(os.path.abspath(logfile))
        self.config = config
        self.writer = writer
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)

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
        terminalreporter.write_sep('-', f'generated testplan file: {self.logfile}', green=True)

    def _save_report(self, report_content: List[dict]) -> None:
        self.writer.write(report_content)


def get_test_name(item: pytest.Item) -> str:
    """Return suite name."""
    if hasattr(item, 'cls') and item.cls:
        return f'{item.module.__name__}::{item.cls.__name__}'
    elif hasattr(item, 'module') and hasattr(item.module, '__name__'):
        return f'{item.module.__name__}'
    elif isinstance(item, YamlFunction):
        return item.function.spec.name
    return ''


def get_item_type(item: pytest.Item) -> str:
    """Return test type."""
    if isinstance(item, YamlFunction):
        return item.function.spec.type
    return ''


def get_item_platform_allow(item: pytest.Item) -> str:
    """Return allowed platforms."""
    if isinstance(item, YamlFunction):
        return ' '.join(item.function.spec.platform_allow)
    return ''


def get_item_tags(item: pytest.Item) -> str:
    """Return comma separated tags."""
    if isinstance(item, YamlFunction):
        return ' '.join(item.function.spec.tags)
    return ''
