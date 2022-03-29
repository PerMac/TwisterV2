from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Any, Generator
from pathlib import Path

import pytest
import yaml

# TODO: remove
DEFAULT_PLATFORMS: str = 'qemu_cortex_m3 qemu_x86 nrf51dk_nrf51422'

logger = logging.getLogger(__name__)


@dataclass
class TwisterConfig:
    """Store twister configuration to have easy access in test."""
    build_only: bool = False
    platforms: list[PlatformConfig] = field(default_factory=list)
    default_platforms: list[str] = field(default_factory=list)
    board_root: list = field(default_factory=list)

    @classmethod
    def create(cls, config: pytest.Config) -> TwisterConfig:
        """Create new instance from pytest.Config."""
        build_only: bool = config.getoption('--build-only')
        default_platforms: list[str] = config.getoption('--platform')
        board_root: list[str] = config.getoption('--board-root')
        platforms = config._platforms

        if not default_platforms:
            default_platforms = [platform.identifier for platform in platforms]

        data: dict[str, Any] = dict(
            build_only=build_only,
            platforms=platforms,
            default_platforms=default_platforms,
            board_root=board_root,
        )
        logger.debug('TwisterConfiguration: %s', data)
        return cls(**data)

    def asdict(self) -> dict:
        """Return dictionary which can be serialized as Json."""
        return dict(
            build_only=self.build_only,
            default_platforms=self.default_platforms,
            board_root=self.board_root
        )


@dataclass
class PlatformConfig:
    """Store platform configuration."""
    # https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/pylib/twister/twisterlib.py#L1601
    identifier: str = ''  # name
    name: str = ''
    twister: bool = True
    ram: int = 128  # in kilobytes
    ignore_tags: list = field(default_factory=list)
    only_tags: list = field(default_factory=list)
    default: bool = False
    flash: int = 512  # in kilobytes
    supported: set = field(default_factory=set)
    arch: str = ''
    type: str = 'na'
    simulation: str = 'na'
    toolchain: list = field(default_factory=list)  # supported_toolchains
    env: list = field(default_factory=list)
    env_satisfied: dict = True
    filter_data: dict = field(default_factory=dict)

    @classmethod
    def load_from_yaml(cls, filename: str) -> PlatformConfig:
        """Load platform from yaml file."""
        with open(filename, 'r', encoding='UTF-8') as file:
            data: dict = yaml.safe_load(file)
            testing = data.pop('testing', None)
            if testing:
                data.update(testing)
        return cls(**data)


def discover_platforms(directory: Path) -> Generator[PlatformConfig, None, None]:
    """Return platforms from given directory"""
    for file in directory.glob('*/*/*.yaml'):
        try:
            yield PlatformConfig.load_from_yaml(str(file))
        except Exception as e:
            logger.exception('Cannot read platform definition from yaml: %e', e)
            raise
