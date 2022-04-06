from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any

import pytest

from twister2.platform_specification import PlatformSpecification

logger = logging.getLogger(__name__)


@dataclass
class TwisterConfig:
    """Store twister configuration to have easy access in test."""
    zephyr_base: str
    build_only: bool = False
    platforms: list[PlatformSpecification] = field(default_factory=list)
    default_platforms: list[str] = field(default_factory=list)
    board_root: list = field(default_factory=list)
    twister_out: str = 'twister-out'

    @classmethod
    def create(cls, config: pytest.Config) -> TwisterConfig:
        """Create new instance from pytest.Config."""
        zephyr_base = config.getoption('zephyr_base') or config.getini('zephyr_base') or os.environ.get('ZEPHYR_BASE')
        build_only: bool = config.getoption('--build-only')
        default_platforms: list[str] = config.getoption('--platform')
        board_root: list[str] = config.getoption('--board-root')
        platforms = config._platforms
        output_dir: str = config.getoption('--outdir')

        if not default_platforms:
            default_platforms = [platform.identifier for platform in platforms]

        data: dict[str, Any] = dict(
            zephyr_base=zephyr_base,
            build_only=build_only,
            platforms=platforms,
            default_platforms=default_platforms,
            board_root=board_root,
            twister_out=output_dir,
        )
        return cls(**data)

    def asdict(self) -> dict:
        """Return dictionary which can be serialized as Json."""
        return dict(
            build_only=self.build_only,
            default_platforms=self.default_platforms,
            board_root=self.board_root
        )
