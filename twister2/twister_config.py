from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any

import pytest

from twister2.device.hardware_map import HardwareMap
from twister2.platform_specification import PlatformSpecification

logger = logging.getLogger(__name__)


@dataclass
class TwisterConfig:
    """Store twister configuration to have easy access in test."""
    zephyr_base: str
    output_dir: str = 'twister-out'
    board_root: list = field(default_factory=list)
    build_only: bool = False
    default_platforms: list[str] = field(default_factory=list)
    platforms: list[PlatformSpecification] = field(default_factory=list, repr=False)
    hardware_map_list: list[HardwareMap] = field(default_factory=list, repr=False)

    @classmethod
    def create(cls, config: pytest.Config) -> TwisterConfig:
        """Create new instance from pytest.Config."""
        zephyr_base = config.getoption('zephyr_base') or config.getini('zephyr_base') or os.environ.get('ZEPHYR_BASE')
        build_only: bool = config.getoption('--build-only')
        default_platforms: list[str] = config.getoption('--platform')
        board_root: list[str] = config.getoption('--board-root')
        platforms = config._platforms
        output_dir: str = config.getoption('--outdir')
        hardware_map_file = config.getoption('--hardware-map')

        hardware_map_list: list[HardwareMap] = []
        if hardware_map_file:
            hardware_map_list = HardwareMap.read_from_file(filename=hardware_map_file)

        if not default_platforms:
            default_platforms = [platform.identifier for platform in platforms]

        data: dict[str, Any] = dict(
            zephyr_base=zephyr_base,
            build_only=build_only,
            platforms=platforms,
            default_platforms=default_platforms,
            board_root=board_root,
            twister_out=output_dir,
            hardware_map_list=hardware_map_list,
        )
        return cls(**data)

    def asdict(self) -> dict:
        """Return dictionary which can be serialized as Json."""
        return dict(
            build_only=self.build_only,
            default_platforms=self.default_platforms,
            board_root=self.board_root,
            output_dir=self.output_dir,
        )
