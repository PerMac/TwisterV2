# from pathlib import Path

# import pytest
# # import hamcrest
# from twister2.yaml_file_parser import (YamlTestSpecification,
#                                        _read_test_specifications_from_yaml)

# yaml_file_path: Path = Path(__file__).parent / 'data' / 'sample1.yaml'


# @pytest.skip('WIP')
# def test_foo():
#     expected_tests = [
#         YamlTestSpecification(
#             name='sample.kernel.philosopher',
#             path=Path('C:/Users/lufu/workspace/temp/twister2/tests/data'),
#             tags='introduction',
#             filter='',
#             min_flash='',
#             build_only=False,
#             harness='console',
#             extra_configs=[] ,
#             extra_args='DEBUG_PRINTF=1',
#             integration_platforms=['native_posix'],
#             platform_allow=[] ,
#             platform_exclude=[],
#             harness_config={'type': 'multi_line', 'ordered': False, 'regex': [
#                 '.*STARVING.*', '.*DROPPED ONE FORK.*', '.*THINKING.*', '.*EATING.*']}
#         ),
#         YamlTestSpecification(
#             name='sample.kernel.philosopher.same_prio',
#             path=Path('C:/Users/lufu/workspace/temp/twister2/tests/data'),
#             tags='introduction',
#             filter='',
#             min_flash='',
#             build_only=False,
#             harness='console',
#             extra_configs=[] ,
#             extra_args='DEBUG_PRINTF=1',
#             integration_platforms=['native_posix'],
#             platform_allow=[],
#             platform_exclude=[] ,
#             harness_config={'type': 'multi_line', 'ordered': False, 'regex': [
#                 '.*STARVING.*', '.*DROPPED ONE FORK.*', '.*THINKING.*', '.*EATING.*']}
#         ),
#         YamlTestSpecification(
#             name='sample.kernel.philosopher.coop_only',
#             path=Path('C:/Users/lufu/workspace/temp/twister2/tests/data'),
#             tags='introduction',
#             filter='',
#             min_flash='',
#             build_only=False,
#             harness='console',
#             extra_configs=['CONFIG_NUM_PREEMPT_PRIORITIES=0', 'CONFIG_NUM_COOP_PRIORITIES=7'],
#             extra_args='DEBUG_PRINTF=1',
#             integration_platforms=['native_posix'],
#             platform_allow=[] ,
#             platform_exclude=[] ,
#             harness_config={'type': 'multi_line', 'ordered': False, 'regex': [
#                 '.*STARVING.*', '.*DROPPED ONE FORK.*', '.*THINKING.*', '.*EATING.*']}
#         )
#     ]

#     test_specifications = _read_test_specifications_from_yaml(yaml_file_path)
#     # assert test_specifications == expected_tests
#     # hamcrest.assert_that(test_specifications, hamcrest.has_item(expected_tests[0]))
