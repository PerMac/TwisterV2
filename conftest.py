import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='test.log',
    filemode='w',
)

pytest_plugins = (
    'twister2.plugin',
    'twister2.yaml_specification',
    'twister2.yaml_specification2',
)
