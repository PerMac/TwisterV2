from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class YamlTestSpecification:
    """Test specification for yaml test."""
    name: str  #: test case name
    path: Path  #: path to a folder where C files are stored
    platform: str  #: platform name used for this test
    tags: set = field(default_factory=set)
    type: str = 'integration'
    filter: str = ''
    min_flash: int = 32
    arch_allow: set = field(default_factory=set)
    arch_exclude: set = field(default_factory=set)
    build_only: bool = False
    build_on_all: bool = False
    skip: bool = False
    slow: bool = False
    timeout: int = 60
    min_ram: int = 8
    depends_on: set = field(default_factory=set)
    harness: str = ''
    extra_sections: list = field(default_factory=list)
    extra_configs: list[str] = field(default_factory=list)
    extra_args: list[str] = field(default_factory=list)
    integration_platforms: list = field(default_factory=list)
    platform_allow: set = field(default_factory=set)
    platform_exclude: set = field(default_factory=set)
    harness_config: dict = field(default_factory=dict)
    toolchain_exclude: set = field(default_factory=set)
    toolchain_allow: set = field(default_factory=set)

    def __post_init__(self):
        if isinstance(self.tags, str):
            self.tags = set(self.tags.split(' '))
        if isinstance(self.platform_allow, str):
            self.platform_allow = set(self.platform_allow.split(' '))
