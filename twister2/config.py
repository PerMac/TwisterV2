import pytest


class TwisterConfig:
    """Store twister configuration to have easy access in test."""

    def __init__(self, config: pytest.Config):
        self.build_only: bool = config.getoption('--build-only')
        self.platform: list = config.getoption('--platform').split(',')  # TODO: platform or platforms?
