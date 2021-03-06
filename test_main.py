import pytest

from main import ts2block


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (1232103989, 693),
        (1231006505, 0),
        (1231006506, 0),
        (1231006507, 0),
        (1234000000, 3344),
        # (1323073003, 156113), this is an edge case not covered t1 > t2
        (1241006505, 12633),
        (1637430034, 710592),
    ],
)
def test_ts2block(test_input, expected):
    assert ts2block(test_input, True) == expected
