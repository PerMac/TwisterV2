import logging
from pathlib import Path

import pytest

from twister2.config import DEFAULT_PLATFORMS, TwisterConfig
from twister2.report.test_plan_csv import CsvTestPlan
from twister2.report.test_plan_json import JsonTestPlan
from twister2.report.test_plan_plugin import TestPlanPlugin
from twister2.yaml_file_parser import YamlFile

SAMPLE_FILENAME: str = 'sample.yaml'
TESTCASE_FILENAME: str = 'testcase.yaml'

logger = logging.getLogger(__name__)

# include fixtures
pytest_plugins = (
    'twister2.fixtures.builder',
    'twister2.fixtures.log_parser',
)


def pytest_collect_file(parent, path):
    # discovers all yaml tests in test directory
    if path.basename in (SAMPLE_FILENAME, TESTCASE_FILENAME):
        return YamlFile.from_parent(parent, path=Path(path))


def pytest_addoption(parser: pytest.Parser):
    custom_reports = parser.getgroup('Twister reports')
    custom_reports.addoption(
        '--testplan',
        dest='testplan_path',
        metavar='path',
        action='store',
        default=None,
        help='generate test plan in CSV format'
    )
    custom_reports.addoption(
        '--testplan-json',
        dest='testplan_json_path',
        metavar='path',
        action='store',
        default=None,
        help='generate test plan in JSON format'
    )

    twister_group = parser.getgroup('Twister')
    twister_group.addoption(
        '--build-only',
        default=False,
        action='store_true',
        help='build only'
    )
    twister_group.addoption(
        '--platform',
        default=DEFAULT_PLATFORMS,
        action='store',
        help='filter test with platform'
    )


def pytest_configure(config: pytest.Config):
    # configure TestPlan plugin
    test_plan_writers = []
    if testplan_csv_path := config.getoption('testplan_path'):
        test_plan_writers.append(CsvTestPlan(testplan_csv_path))
    if testplan_json_path := config.getoption('testplan_json_path'):
        test_plan_writers.append(JsonTestPlan(testplan_json_path))

    if test_plan_writers and not hasattr(config, 'workerinput'):
        config.pluginmanager.register(
            plugin=TestPlanPlugin(config=config, writers=test_plan_writers),
            name='testplan'
        )

    config.twister_config = TwisterConfig(config)

    # register filter plugin
    # config.pluginmanager.register(plugin=FilterPlugging(config), name='filter plugin')
