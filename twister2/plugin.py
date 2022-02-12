import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def dut(request: pytest.FixtureRequest):
    logger.info('Dut fixture...')
    logger.info(request.config.args)
    return dict(name='dut1')
