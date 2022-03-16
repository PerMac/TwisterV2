import pytest

from twister2.yaml_test_class import YamlFunction


def is_yaml_test(item: pytest.Item) -> bool:
    """Return True if item is a yaml test."""
    if isinstance(item, YamlFunction):
        return True
    else:
        return False
