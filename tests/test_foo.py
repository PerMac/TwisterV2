import logging

from twister2 import TwisterSpec, load_c_test

logger = logging.getLogger(__name__)


@load_c_test(path=r'tests/test_bar.yaml')
def test_foo(spec: TwisterSpec):
    logger.info(f'Runing test {spec}')
    spec.run_test()
    spec.assert_result()
