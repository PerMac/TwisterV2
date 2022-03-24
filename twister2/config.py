from __future__ import annotations

import logging
from dataclasses import dataclass, asdict, field
from typing import Any
import pytest

# hardcoded for PoC
DEFAULT_PLATFORMS: str = 'qemu_cortex_m3 qemu_x86 nrf51dk_nrf51422'

logger = logging.getLogger(__name__)


@dataclass
class TwisterConfig:
    """Store twister configuration to have easy access in test."""
    build_only: bool = False
    platforms: list = field(default_factory=list)

    @classmethod
    def create(cls, config: pytest.Config) -> TwisterConfig:
        """Create new instance from pytest.Config."""
        build_only: bool = config.getoption('--build-only')
        platforms_string: str = config.getoption('--platform')
        if ',' in platforms_string:
            platforms = platforms_string.split(',')
        else:
            platforms = platforms_string.split()

        data: dict[str, Any] = dict(
            build_only=build_only,
            platforms=platforms,
        )
        logger.debug('TwisterConfiguration: %s', data)
        return cls(**data)

    def asdict(self) -> dict:
        return asdict(self)
