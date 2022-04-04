from __future__ import annotations

import logging

import pytest

from twister2.log_parser.factory import LogParserFactory
from twister2.log_parser.harness_log_parser import HarnessLogParser
from twister2.yaml_test_function import YamlTestCase
from twister2.exceptions import TwisterRunException

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def log_parser(request: pytest.FixtureRequest, dut) -> HarnessLogParser | None:
    """Return log parser."""
    if not isinstance(request.function, YamlTestCase):
        yield

    harness = getattr(request.function.spec, 'harness', 'harness')
    if dut.log_file.exists():
        with open(dut.log_file, 'r', encoding='UTF-8') as file:
            yield LogParserFactory.get_parser(harness)(file)
    else:
        logger.exception('Log file not exists: %s', dut.log_file)
        raise TwisterRunException(f'Log file not exists: {dut.log_file}')
