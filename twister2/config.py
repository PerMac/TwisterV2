import logging

import pytest

# hardcoder for PoC
DEFAULT_PLATFORMS: str = 'qemu_cortex_m3 qemu_x86 nrf51dk_nrf51422'

logger = logging.getLogger(__name__)


# TODO: replace by dataclass and add factory method to build from pytest.Config
class TwisterConfig:
    """Store twister configuration to have easy access in test."""

    def __init__(self, config: pytest.Config):
        self.build_only: bool = config.getoption('--build-only')
        platforms = config.getoption('--platform')
        if ',' in platforms:
            platforms = platforms.split(',')
        else:
            platforms = platforms.split()
        self.platforms: list = platforms
        logger.debug('TwisterConfiguration: %s', self)

    def __str__(self):
        return f'{self.__class__.__name__}<build_only={self.build_only}, platform={self.platforms}>'
