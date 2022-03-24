import pytest
from twister2.yaml_test_class import YamlTestFunction


def get_suite_name(item: pytest.Item) -> str:
    """Return suite name."""
    if hasattr(item, 'cls') and item.cls:
        return f'{item.module.__name__}::{item.cls.__name__}'
    elif hasattr(item, 'module') and hasattr(item.module, '__name__'):
        return f'{item.module.__name__}'
    elif isinstance(item, YamlTestFunction):
        # TODO: define what is suite to yaml test
        return item.parent.nodeid
    return item.parent.nodeid


def get_test_name(item: pytest.Item) -> str:
    """Return test name."""
    return item.name


def get_test_path(item: pytest.Item) -> str:
    """Return path to file where test is defined."""
    return item.parent.nodeid


def get_item_type(item: pytest.Item) -> str:
    """Return test type."""
    if isinstance(item, YamlTestFunction):
        return item.function.spec.type
    return ''


def get_item_platform_allow(item: pytest.Item) -> str:
    """Return allowed platforms."""
    if isinstance(item, YamlTestFunction):
        return ' '.join(item.function.spec.platform_allow)
    return ''


def get_item_tags(item: pytest.Item) -> str:
    """Return comma separated tags."""
    if isinstance(item, YamlTestFunction):
        return ' '.join(item.function.spec.tags)
    return ''
