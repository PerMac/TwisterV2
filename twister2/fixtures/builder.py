"""
Pytest fixture for building hex files.
"""
import logging
from pathlib import Path

import pytest

from twister2.builder.builder_abstract import BuilderAbstract
from twister2.builder.factory import BuilderFactory
from twister2.twister_config import TwisterConfig

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def builder(request: pytest.FixtureRequest) -> BuilderAbstract:
    """Build hex files for test suite."""
    twister_config: TwisterConfig = request.config.twister_config
    function = request.function
    builder_klass = BuilderFactory.get_builder('west')
    builder = builder_klass(zephyr_base=twister_config.zephyr_base, source_dir=function.spec.path)
    build_dir = Path(twister_config.output_dir) / function.spec.platform / request.node.originalname.replace('.', '/')
    builder.build(
        platform=function.spec.platform,
        build_dir=build_dir,
        cmake_args=function.spec.extra_args,
    )
    yield builder


def get_relative_path(path1: str, path2: str) -> str:
    """Return relative path to other path."""
    path1 = str(Path(path1).resolve())
    path2 = str(Path(path2).resolve())
    return path2.replace(path1, '')
