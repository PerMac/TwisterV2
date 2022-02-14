import logging
from pathlib import Path

import pytest
import yaml

logger = logging.getLogger(__name__)


def pytest_collect_file(parent, path):
    if path.ext == ".yaml" and path.basename.startswith("test"):
        return YamlFile.from_parent(parent, path=Path(path))


class YamlFile(pytest.File):

    def collect(self):
        raw = yaml.safe_load(self.path.open())
        for name, spec in sorted(raw.items()):
            yield YamlItem.from_parent(self, name=name, spec=spec)


class YamlItem(pytest.Item):

    def __init__(self, name, parent, spec):
        super().__init__(name, parent)
        self.spec = spec

    def setup(self) -> None:
        super().setup()
        logger.info('setup %s', repr(self))

    def teardown(self) -> None:
        super().teardown()
        logger.info('teardown %s', repr(self))

    def runtest(self):
        for name, value in sorted(self.spec.items()):
            # Some custom test execution (dumb example follows).
            if name != value:
                raise YamlException(self, name, value)

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, YamlException):
            return "\n".join(
                [
                    "usecase execution failed",
                    "   spec failed: {1!r}: {2!r}".format(*excinfo.value.args),
                    "   no further details known at this point.",
                ]
            )

    def reportinfo(self):
        return self.path, 0, f"usecase: {self.name}"


class YamlException(Exception):
    """Custom exception for error reporting."""
