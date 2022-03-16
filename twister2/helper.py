import pytest


def is_yaml_test(item: pytest.Item) -> bool:
    """Return True if item is a yaml test."""
    if hasattr(item.function, 'spec'):
        return True
    else:
        return False
