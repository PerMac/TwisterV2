import os
from typing import List

import pytest
from _pytest.terminal import TerminalReporter

from .test_plan_csv import CsvTestPlan


def get_suite_name(item: pytest.Item) -> str:
    """Return suite name"""
    if hasattr(item, 'cls') and item.cls:
        return f'{item.module.__name__}::{item.cls.__name__}'
    elif hasattr(item, 'module'):
        return f'{item.module.__name__}'
    else:
        return item.path


class TestPlanPlugin:
    """
    Generate TestPlan as CSV.

    :param logfile: output filename
    :param config: pytest._Config
    """

    def __init__(self, logfile: str, config: pytest.Config):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.normpath(os.path.abspath(logfile))
        self.config = config
        self.writer = CsvTestPlan(self.logfile)
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)

    def _item_as_dict(self, item: pytest.Item) -> dict:

        return dict(
            suite_name=get_suite_name(item),
            test_name=item.name,
            markers='',
            tags='',
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
        terminalreporter.ensure_newline()
        terminalreporter.write_sep('-', f'generated testplan file: {self.logfile}', green=True)

    def _save_report(self, report_content: List[dict]) -> None:
        self.writer.write(report_content)
