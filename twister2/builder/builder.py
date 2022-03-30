import pytest
import logging

logger = logging.getLogger(__name__)


class Builder:

    def __init__(self, config: pytest.Config):
        """
        :param config: pytest configuration
        """
        self.config = config
        self.twister_config = config.twister_config

    def build(self, function):
        logger.info('Running cmake on %s for %s', function.spec.path, function.spec.platform)
