"""
Pytest fixture for building hex files.
"""
import logging

import pytest
from twister2.yaml_test_class import YamlTestClass

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function', autouse=True)
def builder(request: pytest.FixtureRequest) -> None:
    """Build hex files for test suite."""
    if isinstance(request.function, YamlTestClass):
        function = request.function
        twister_config = request.config.twister_config
        logger.info('Running cmake on %s for %s', function.spec.path, function.spec.platform)
    yield
