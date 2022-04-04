import logging
from pathlib import Path

import pytest

from twister2.builder.builder_abstract import BuilderAbstract
from twister2.device.device_abstract import DeviceAbstract
from twister2.device.factory import DeviceFactory

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def dut(request: pytest.FixtureRequest, builder: BuilderAbstract) -> DeviceAbstract:
    twister_config = request.config.twister_config
    function = request.function
    build_dir = Path(twister_config.twister_out) / function.spec.platform / request.node.originalname.replace('.', '/')

    device = DeviceFactory.get_device('simulator')()  # TODO:
    device.connect()
    device.flash(build_dir=build_dir)
    yield device
    device.disconnect()
