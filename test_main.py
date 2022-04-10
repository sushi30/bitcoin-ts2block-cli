import pytest

from main import ts2block


@pytest.mark.parametrize(
    "test_input,expected",
    [(1232103989, 693), (1637430034, 710592), (1231006505, 0), (1234000000, 3344)],
)
def test_ts2block(test_input, expected):
    assert ts2block(test_input, True) == expected
