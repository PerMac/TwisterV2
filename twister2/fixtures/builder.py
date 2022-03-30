"""
Pytest fixture for building hex files.
"""
import logging

import pytest

from twister2.builder.builder import Builder
from twister2.yaml_test_function import YamlTestCase

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function', autouse=False)
def builder(request: pytest.FixtureRequest) -> Builder:
    """Build hex files for test suite."""
    if isinstance(request.function, YamlTestCase):
        function = request.function
        builder = Builder(request.config)
        builder.build(function)
        yield builder
    else:
        yield None
