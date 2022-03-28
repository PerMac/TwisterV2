import logging
from pathlib import Path
import os

import pytest
from twister2.config import TwisterConfig, discover_platforms
from twister2.report.test_plan_csv import CsvTestPlan
from twister2.report.test_plan_json import JsonTestPlan
from twister2.report.test_plan_plugin import TestPlanPlugin
from twister2.report.test_results_json import JsonResultsReport
from twister2.report.test_results_plugin import TestResultsPlugin
from twister2.yaml_file import YamlFile

SAMPLE_FILENAME: str = 'sample.yaml'
TESTCASE_FILENAME: str = 'testcase.yaml'
ZEPHYR_BASE = os.environ.get('ZEPHYR_BASE')  # TODO: raise an exception if not set
# Directory to search for board configuration files. All .yaml
# files in the directory will be processed. The directory should have the same
# structure in the main Zephyr tree: boards/<arch>/<board_name>/
board_root_list = [
    f'{ZEPHYR_BASE}/boards',
    f'{ZEPHYR_BASE}/scripts/pylib/twister/boards',
]

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
        '--testplan-csv',
        dest='testplan_csv_path',
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
    custom_reports.addoption(
        '--results-json',
        dest='results_json_path',
        metavar='path',
        action='store',
        default=None,
        help='generate test results report in JSON format'
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
        action='append',
        help='build tests for specific platforms'
    )
    twister_group.addoption(
        '--board-root',
        action='append',
        default=board_root_list,
        help='directory to search for board configuration files'
    )


def pytest_configure(config: pytest.Config):
    # configure TestPlan plugin
    test_plan_writers = []
    if testplan_csv_path := config.getoption('testplan_csv_path'):
        test_plan_writers.append(CsvTestPlan(testplan_csv_path))
    if testplan_json_path := config.getoption('testplan_json_path'):
        test_plan_writers.append(JsonTestPlan(testplan_json_path))

    if test_plan_writers and not hasattr(config, 'workerinput'):
        config.pluginmanager.register(
            plugin=TestPlanPlugin(config=config, writers=test_plan_writers),
            name='testplan'
        )

    test_results_writers = []
    if test_result_json_path := config.getoption('results_json_path'):
        test_results_writers.append(JsonResultsReport(test_result_json_path))

    if test_results_writers and not hasattr(config, 'workerinput') and not config.option.collectonly:
        config.pluginmanager.register(
            plugin=TestResultsPlugin(config, writers=test_results_writers),
            name='test-results'
        )

    board_root = config.getoption('board_root')
    default_platforms: list[str] = []
    for directory in board_root:
        for platform_config in discover_platforms(Path(directory)):
            default_platforms.append(platform_config.identifier)
    config._default_platforms = default_platforms

    config.twister_config = TwisterConfig.create(config)
