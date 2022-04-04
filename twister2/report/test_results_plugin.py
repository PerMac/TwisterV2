from __future__ import annotations

import platform
import time
from collections import Counter

import pytest
from pytest_subtests import SubTestReport

from twister2.report.base_report_writer import BaseReportWriter
from twister2.report.helper import (
    get_item_platform_allow,
    get_item_tags,
    get_item_type,
    get_suite_name,
    get_test_name,
    get_item_platform
)


class Status:
    PASSED = 'passed'
    XPASSED = 'xpassed'
    FAILED = 'failed'
    XFAILED = 'xfailed'
    ERROR = 'error'
    SKIPPED = 'skipped'
    RERUN = 'rerun'


class TestResult:
    """Class stores test result for single test."""

    def __init__(self, outcome: str, report: pytest.TestReport, config: pytest.Config):
        self.test_id: str = report.nodeid.encode('utf-8').decode('unicode_escape')
        self.nodeid = report.nodeid
        self.name: str = self.test_id
        if getattr(report, 'when', 'call') != 'call':
            self.test_id = '::'.join([report.nodeid, report.when])
        self.status = outcome
        self.item = report.nodeid
        self.report = report
        self.config = config
        self.duration: float = getattr(report, 'duration', 0.0)
        # self.message: str = report.longrepr
        self.message: str = report.longreprtext
        self.subtests: list = []

    def __repr__(self):
        return f'{self.__class__.__name__}({self.status!r})'

    def add_subtest(self, subtest):
        order = (
            Status.PASSED,
            Status.SKIPPED,
            Status.XPASSED,
            Status.XFAILED,
            Status.RERUN,
            Status.FAILED,
            Status.ERROR,
        )
        status = order[max(order.index(self.status), order.index(subtest['status']))]
        self.status = status
        self.subtests.append(subtest)


class TestResultsPlugin:
    """Class collects results and crates result report."""

    def __init__(self, config: pytest.Config, writers: list[BaseReportWriter]):
        """
        :param config: pytest configuration
        :param writers: list of report writers
        """
        self.config = config
        self.writers = writers
        self.counter = Counter(passed=0, failed=0, skipped=0, xfailed=0, xpassed=0, error=0)
        self.test_results: dict[str, TestResult] = {}
        self.items: dict[str, pytest.Item] = {}

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        if report.when == 'call':
            if item.nodeid not in self.items:
                self.items[item.nodeid] = item

    def pytest_runtest_logreport(self, report: pytest.TestReport):
        outcome = self._get_outcome(report)
        if not outcome:
            return

        if report.nodeid not in self.test_results:
            self.test_results[report.nodeid] = TestResult(outcome, report, self.config)
        if self._is_sub_test(report):
            self.test_results[report.nodeid].add_subtest(dict(name=report.context.msg, status=outcome))

    def _is_sub_test(self, report: pytest.Report) -> bool:
        return isinstance(report, SubTestReport)

    def pytest_sessionstart(self, session: pytest.Session):
        self.session_start_time = time.time()

    def pytest_sessionfinish(self, session: pytest.Session):
        self.session_stop_time = time.time()
        data = self._generate_report(session)
        self._save_report(data)

    def pytest_terminal_summary(self, terminalreporter):
        for writer in self.writers:
            terminalreporter.write_sep(
                '-', f'generated results report file: {writer.filename}', green=True
            )

    def _get_outcome(self, report: pytest.TestReport) -> str | None:
        if report.failed:
            if report.when != 'call':
                return Status.ERROR
            elif hasattr(report, 'wasxfail'):
                return Status.XPASSED
            else:
                return Status.FAILED
        elif report.skipped:
            if hasattr(report, 'wasxfail'):
                return Status.XFAILED
            else:
                return Status.SKIPPED
        elif report.passed and report.when == 'call':
            return Status.PASSED

    def _generate_report(self, session: pytest.Session) -> dict:
        """Return rendered report as string"""
        tests_list: list = []

        for result in self.test_results.values():
            item = self.items.get(result.nodeid)

            if not item:
                continue

            self.counter[result.status] += 1

            test = dict(
                suite_name=get_suite_name(item),
                test_name=get_test_name(item),
                nodeid=item.nodeid,
                platform=get_item_platform(item),
                tags=get_item_tags(item),
                type=get_item_type(item),
                platform_allow=get_item_platform_allow(item),
                status=result.status,
                message=result.message,
                duration=result.duration,
                subtests=result.subtests,
            )
            tests_list.append(test)

        duration = self.session_stop_time - self.session_start_time
        environment = dict(
            report_time=time.strftime('%H:%M:%S %d-%m-%Y'),
            pc_name=platform.node() or 'N/A',
            duration=duration,
        )
        summary = dict(self.counter)
        summary['total'] = sum(self.counter.values())

        return dict(
            environment=environment,
            configuration=self.config.twister_config.asdict(),
            summary=summary,
            tests=tests_list,
        )

    def _save_report(self, data: dict) -> None:
        for writer in self.writers:
            writer.write(data)
