import pytest
from twister2 import TwisterSpec, load_c_test


@load_c_test(path=r'tests/test_bar.yaml')
def test_foo(spec: TwisterSpec):
    spec.run_test()
    spec.assert_result()
