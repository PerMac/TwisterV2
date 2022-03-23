from pathlib import Path

import pytest

TEST_DIR = Path(__file__).parent


@pytest.fixture()
def yaml_test(testdir):
    testdir.copy_example(TEST_DIR / 'data/testcase.yaml')
    testdir.copy_example(TEST_DIR / 'data/stream.log')
    testdir.makeconftest("pytest_plugins = ('twister2.plugin',)")
    return testdir


def test_twister_help(yaml_test):
    result = yaml_test.runpytest('--help')
    print(result.stdout)
    result.stdout.fnmatch_lines_random([
        '*Twister reports:*',
        '*--testplan=path*generate csv containing test metadata*',
        '*Twister:*',
        '*--build-only*build only*',
        '*--platform=PLATFORM*filter test with platform*',
    ])


def test_twister(yaml_test):
    testplan_file = TEST_DIR / 'twister.csv'
    result = yaml_test.runpytest(
        '-v',
        f'--testplan={str(testplan_file.resolve())}',
    )
    print(result.stdout)
    result.assert_outcomes(passed=3)
    result.stdout.fnmatch_lines_random([
        '*testcase.yaml::bluetooth.mesh.mesh_shell*qemu_cortex_m3*PASSED*',
        '*testcase.yaml::bluetooth.mesh.mesh_shell*qemu_x86*PASSED*',
        '*testcase.yaml::bluetooth.mesh.mesh_shell*nrf51dk_nrf51422*PASSED*',
        '*generated testplan file:*twister.csv*',
    ])
