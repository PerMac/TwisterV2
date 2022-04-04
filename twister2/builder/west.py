from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from twister2.builder.builder_abstract import BuilderAbstract
from twister2.exceptions import TwisterBuilderException

logger = logging.getLogger(__name__)


class WestBuilder(BuilderAbstract):

    def flash(self, build_dir: str | Path, **kwargs) -> None:
        """
        Permanently reprogram a board's flash with a new binary.

        :param build_dir: application build directory
        """
        command = [
            'west',
            'flash',
            '--skip-rebuild',
            '--build-dir', str(build_dir),
        ]

        logger.info('Flashing device')
        logger.info('Flashing command: %s', ' '.join(command))
        try:
            process = subprocess.run(
                command,
                check=True,
                text=True,
                cwd=self.zephyr_base.resolve(),
                env=self.env,
            )
        except subprocess.CalledProcessError as e:
            logger.error('Error while flashing')
            raise TwisterBuilderException('Flashing error') from e
        else:
            if process.returncode == 0:
                logger.info('Finished flashing %s', build_dir)

    def build(self, platform: str, build_dir: str | Path = None, **kwargs) -> None:
        """
        Build Zephyr application.

        :param platform: board to build for with optional board revision
        :param build_dir: build directory to create or use
        :keyword cmake_args: list of extra cmake arguments
        """
        command = [
            'west',
            'build',
            '--pristine', 'always',
            '--board', platform,
            str(self.source_dir),
        ]
        if build_dir:
            command.extend(['--build-dir', str(build_dir)])
        if cmake_args := kwargs.get('cmake_args'):
            args = self._prepare_cmake_args(cmake_args)
            command.extend(['--', args])

        logger.info('Building Zephyr application')
        logger.info('Build command: %s', ' '.join(command))
        try:
            process = subprocess.run(
                command,
                capture_output=False,
                check=True,
                text=True,
                cwd=self.zephyr_base.resolve(),
                env=self.env,
            )
        except subprocess.CalledProcessError as e:
            logger.error('Failed building %s for %s', self.source_dir, platform)
            raise TwisterBuilderException('Building error') from e
        else:
            if process.returncode == 0:
                logger.info('Finished building %s for %s', self.source_dir, platform)

    @staticmethod
    def _prepare_cmake_args(cmake_args: list[str]) -> str:
        args_joined = ' '.join([f'-D{arg}' for arg in cmake_args])
        return f'"{args_joined}"'
