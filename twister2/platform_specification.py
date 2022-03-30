from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator

import pytest
import yaml

logger = logging.getLogger(__name__)


@dataclass
class PlatformSpecification:
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
    def load_from_yaml(cls, filename: str) -> PlatformSpecification:
        """Load platform from yaml file."""
        with open(filename, 'r', encoding='UTF-8') as file:
            data: dict = yaml.safe_load(file)
            testing = data.pop('testing', None)
            if testing:
                data.update(testing)
        return cls(**data)


def discover_platforms(directory: Path) -> Generator[PlatformSpecification, None, None]:
    """Return platforms from given directory"""
    for file in directory.glob('*/*/*.yaml'):
        try:
            yield PlatformSpecification.load_from_yaml(str(file))
        except Exception as e:
            logger.exception('Cannot read platform definition from yaml: %e', e)
            raise


def validate_platforms_list(platforms: list[PlatformSpecification]) -> None:
    """Validate platforms."""
    # varify duplications
    duplicated: list[str] = []
    platforms_list: list[str] = []
    for platform in platforms:
        if platform.identifier in platforms_list:
            duplicated.append(platform.identifier)
        else:
            platforms_list.append(platform.identifier)
    if len(duplicated) != 0:
        pytest.exit(f'There are duplicated platforms: {", ".join(duplicated)}')
