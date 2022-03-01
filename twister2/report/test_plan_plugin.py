"""
Plugin to generate test plan report
"""
from __future__ import annotations

import os
from typing import List, Protocol

import pytest
from _pytest.terminal import TerminalReporter

from .test_plan_csv import CsvTestPlan


def get_suite_name(item: pytest.Item) -> str:
    """Return suite name"""
    if hasattr(item, 'cls') and item.cls:
        return f'{item.module.__name__}::{item.cls.__name__}'
    elif hasattr(item, 'module') and hasattr(item.module, '__name__'):
        return f'{item.module.__name__}'
    else:
        return item.path


def get_item_specification(item: pytest.Item) -> dict:
    return getattr(item, 'spec', {})


class SpecReportInterface(Protocol):
    def write(self, data: list[dict]) -> None: ...


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
        spec_report_class: SpecReportInterface | None = None
    ):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.normpath(os.path.abspath(logfile))
        self.config = config
        if spec_report_class:
            writer = spec_report_class(self.logfile)
        else:
            writer = CsvTestPlan(self.logfile)
        self.writer: SpecReportInterface = writer
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)

    def _item_as_dict(self, item: pytest.Item) -> dict:

        return dict(
            suite_name=get_suite_name(item),
            test_name=item.name,
            markers='',
            tags='',
            specification=get_item_specification(item)
        )

    def generate(self, items: List[pytest.Item]):
        """Build test plan and save."""
        rows = [self._item_as_dict(item) for item in items]
        self._save_report(rows)

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]):
        if config.getoption('testplan_path'):
            self.generate(items)

    def pytest_terminal_summary(self, terminalreporter: TerminalReporter) -> None:
        # print summary to terminal
        terminalreporter.ensure_newline()
        terminalreporter.write_sep('-', f'generated testplan file: {self.logfile}', green=True)

    def _save_report(self, report_content: List[dict]) -> None:
        self.writer.write(report_content)
