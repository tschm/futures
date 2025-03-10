import pytest

from futures.bloomberg.month import code2name, name2code


def test_name2code():
    assert name2code("June") == "M"

    with pytest.raises(KeyError):
        name2code("Juno")

def test_code2name():
    assert code2name("M") == "June"

    with pytest.raises(KeyError):
        code2name("T")
