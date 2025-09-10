import dataclasses

from corbel._utils._default_value import default_value


def test_default_value_with_default():
    f = dataclasses.field(default=10)
    assert default_value(f) == 10


def test_default_value_with_default_factory():
    f = dataclasses.field(default_factory=list)
    val = default_value(f)
    assert isinstance(val, list)
    assert val == []


def test_default_value_with_no_default_or_factory():
    f = dataclasses.field()
    assert default_value(f) is None
