import pytest

from twister2.yaml_test_function import YamlTestFunction


def is_yaml_test(item: pytest.Item) -> bool:
    """Return True if item is a yaml test."""
    if isinstance(item, YamlTestFunction):
        return True
    else:
        return False
