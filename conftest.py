import logging

logging.basicConfig(level=logging.DEBUG)

pytest_plugins = (
    'twister2.plugin',
    'twister2.yaml_specification',
)
