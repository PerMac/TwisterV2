from __future__ import annotations

import logging

import pytest

from twister2.log_parser import LogParser
from twister2.yaml_test_function import YamlTestCase
from twister2.exceptions import TwisterRunException

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def log_parser(request: pytest.FixtureRequest, dut) -> LogParser | None:
    """Return log parser."""
    if not isinstance(request.function, YamlTestCase):
        yield

    # mocked log stream
    if dut.log_file.exists():
        yield LogParser(dut.log_file.open())
    else:
        logger.exception('Log file not exists: %s', dut.log_file)
        raise TwisterRunException(f'Log file not exists: {dut.log_file}')
