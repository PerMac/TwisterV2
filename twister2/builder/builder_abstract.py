from __future__ import annotations

import abc
import contextlib
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class BuilderAbstract(abc.ABC):
    """Base class for builders."""

    def __init__(self, zephyr_base: str | Path, source_dir: str | Path):
        self.zephyr_base: Path = Path(zephyr_base)
        self.source_dir: Path = Path(source_dir)

    @property
    def env(self) -> dict[str, str]:
        env = os.environ.copy()
        env['ZEPHYR_BASE'] = str(self.zephyr_base)
        return env

    @abc.abstractmethod
    def build(self, platform: str, build_dir: str | Path = None, **kwargs) -> None:
        """Build Zephyr application."""

    @abc.abstractmethod
    def flash(self, build_dir: str | Path, **kwargs) -> None:
        """Flash device."""

    @contextlib.contextmanager
    def set_directory(self, path: Path) -> None:
        origin = Path().absolute()
        try:
            logger.debug('Changing directory to "%s"', path)
            os.chdir(path)
            yield
        finally:
            os.chdir(origin)
