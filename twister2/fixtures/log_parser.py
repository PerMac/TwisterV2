from __future__ import annotations

import logging
from pathlib import Path

import pytest
from twister2.log_parser import LogParser
from twister2.yaml_test_class import YamlTestClass

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def log_parser(request: pytest.FixtureRequest) -> LogParser | None:
    """Return log parser."""
    if not isinstance(request.function, YamlTestClass):
        yield

    # mocked log stream
    log_file = Path(request.function.spec.path, 'stream.log')
    if log_file.exists():
        yield LogParser(log_file.open())
    else:
        logger.warning('Log file not exists: %s', log_file)
        yield
