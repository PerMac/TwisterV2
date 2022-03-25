"""
Log parser.
"""
from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass
from typing import Iterator, Generator

RUN_PASSED: str = 'PROJECT EXECUTION SUCCESSFUL'
RUN_FAILED: str = 'PROJECT EXECUTION FAILED'
FAULT: str = 'ZEPHYR FATAL ERROR'

# PASS - test_thread_runtime_stats_get in 0.1 seconds
result_re: re.Pattern = re.compile(
    r'^.*(?P<result>PASS|FAIL|SKIP) - (test_)?(?P<testname>.*) in (?P<duration>[0-9\.]+) seconds$'
)
testsuite_name_re: re.Pattern = re.compile(r'^.*Running test suite\s(?P<testsuite>.*)$')

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    testname: str
    result: str
    duration: float

    def __post_init__(self):
        if isinstance(self.duration, str):
            self.duration = float(self.duration)

    def asdict(self) -> dict:
        return asdict(self)


# TODO: implement as async or thread
class LogParser:
    """Parse output from log stream."""

    def __init__(self, stream: Iterator[str]):
        self.stream = stream
        self.stop = False

    def parse(self) -> Generator[TestResult, None, None] | None:
        """Parse logs and return list of tests with statuses."""
        for line in self.stream:
            if RUN_FAILED in line:
                logger.error('PROJECT EXECUTION FAILED')
                break
            if FAULT in line:
                logger.error('ZEPHYR FATAL ERROR')
                break

            if match := testsuite_name_re.match(line):
                test_suite_name = match.group(1)
                logger.debug('Found test suite: %s', test_suite_name)

            if match := result_re.match(line):
                yield TestResult(**match.groupdict())

            if self.stop:
                break


if __name__ == '__main__':
    import pathlib
    from pprint import pprint

    filepath = (pathlib.Path(__file__).parents[1] / 'examples/zephyr_logs/threads_lifecycle.log').resolve()

    parser = LogParser(filepath.open())
    results = parser.parse()
    pprint(list(results))
