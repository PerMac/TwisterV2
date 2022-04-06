"""
Log parser.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Iterator, Generator

from twister2.exceptions import TwisterFatalError
from twister2.log_parser.log_parser_abstract import SubTestResult, LogParserAbstract

RUN_PASSED: str = 'PROJECT EXECUTION SUCCESSFUL'
RUN_FAILED: str = 'PROJECT EXECUTION FAILED'
ZEPHYR_FATAL_ERROR: str = 'ZEPHYR FATAL ERROR'

result_re_pattern: re.Pattern = re.compile(
    r'^.*(?P<result>PASS|FAIL|SKIP) - (test_)?(?P<testname>.*) in (?P<duration>[0-9\.]+) seconds$'
)
testsuite_name_re_pattern: re.Pattern = re.compile(r'^.*Running test suite\s(?P<testsuite>.*)$')

logger = logging.getLogger(__name__)


@dataclass
class HarnessConfig:
    fail_on_fault: bool = False


class HarnessLogParser(LogParserAbstract):
    """Parse output from log stream."""

    def __init__(self, stream: Iterator[str]):
        super().__init__(stream)
        self.config: HarnessConfig = HarnessConfig()
        self.stop: bool = False

    def parse(self) -> Generator[SubTestResult, None, None] | None:
        """Parse logs and return list of tests with statuses."""
        for line in self.stream:
            if RUN_FAILED in line:
                logger.error('PROJECT EXECUTION FAILED')
                self.state = 'FAILED'
                self.messages.append('Project execution failed')

            if RUN_PASSED in line:
                self.state = 'FAILED' if self.state == 'FAILED' else 'PASSED'

            if ZEPHYR_FATAL_ERROR in line:
                logger.error('ZEPHYR FATAL ERROR')
                if self.config.fail_on_fault:
                    raise TwisterFatalError('Zephyr fatal error')

            if match := testsuite_name_re_pattern.match(line):
                test_suite_name = match.group(1)
                logger.info('Found test suite: %s', test_suite_name)

            if match := result_re_pattern.match(line):
                yield SubTestResult(**match.groupdict())

            if self.stop:
                break